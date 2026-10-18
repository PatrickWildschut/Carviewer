import math
import os
import random
import threading
import time
import chess
import chess.pgn
import pygame
# imported first so the "Bye!" overlay is drawn on top of the screensaver
import engine_off
import chessdraw
from chessdraw import (LIGHT_SQUARE, DARK_SQUARE, LIGHT_LAST, DARK_LAST, TEXT_COLOR,
                       DIM_TEXT_COLOR, ACCENT_COLOR, WHITE_PIECE, BLACK_PIECE)

# Chess screensaver: after IDLE_TIME seconds at speed 0 the screen dims and a
# master game is replayed move by move. Games are read from GAMES_FILE (PGN,
# games separated by a blank line) and one is picked at random each time, so
# add as many as you like. A touch wakes it (and is swallowed so it doesn't
# press a button underneath), and so does driving off again.
IDLE_TIME = 60
FADE_TIME = 1.5
MOVE_PAUSE = 1.2        # seconds between moves
MOVE_ANIM = 0.6         # seconds a piece takes to slide
GAME_END_PAUSE = 6      # seconds the result stays up before the next game
MAX_PLIES = 160         # only for the bot fallback
GAMES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chess_games", "games.pgn")

DIM_COLOR = (0, 0, 0)

_games_cache = (None, [])       # (file modification time, games)
_last_pick = None

def _load_games():
    # Reads GAMES_FILE again whenever it changes, so new games show up without
    # restarting. Games with illegal moves or no moves are skipped.
    global _games_cache
    try:
        modified = os.path.getmtime(GAMES_FILE)
    except OSError:
        return []
    if _games_cache[0] == modified:
        return _games_cache[1]

    games = []
    try:
        with open(GAMES_FILE, encoding="utf-8", errors="replace") as file:
            while True:
                game = chess.pgn.read_game(file)
                if game is None:
                    break
                moves = list(game.mainline_moves())
                if moves and not game.errors:
                    games.append((game.headers, game.board(), moves))
    except Exception as error:
        print("Could not read", GAMES_FILE, error)
    _games_cache = (modified, games)
    return games

def _pick_game():
    # a random game, never the same one twice in a row
    global _last_pick
    games = _load_games()
    if not games:
        return None
    choices = [i for i in range(len(games)) if i != _last_pick] or [0]
    _last_pick = random.choice(choices)
    return games[_last_pick]

def _player(headers, key):
    name = headers.get(key, "").strip()
    return name if name and name != "?" else "Unknown"

class _Game:
    def __init__(self):
        self.history = []               # SAN of every move played
        self.last_move = None
        self.anim = None                # (start time, move) while a piece slides
        self.pending = None             # next move, waiting for its turn
        self.next_move_at = time.time() + MOVE_PAUSE
        self.over_at = None             # when the game ended
        self.result_text = ""

        record = _pick_game()
        if record is not None:
            headers, self.board, moves = record
            self.board = self.board.copy()
            self.moves = list(moves)
            self.white = _player(headers, "White")
            self.black = _player(headers, "Black")
            event = headers.get("Event", "").strip()
            event = "" if event in ("", "?") else event
            year = headers.get("Date", "?")[:4]
            if year.isdigit() and year not in event:
                event = (event + ", " + year).lstrip(", ")
            self.info = event
            self.result = headers.get("Result", "*")
            self.bot = False
        else:
            # no games file: the bot plays itself so there is still something to see
            import chessbot
            self.board = chess.Board()
            self.moves = []
            self.opening = random.choice(list(chessbot.OPENINGS))
            self.book = chessbot.OPENINGS[self.opening].split()
            self.white = self.black = "Bot"
            self.info = self.opening
            self.result = "*"
            self.bot = True
        self._think()

    def _think(self):
        if not self.bot:
            if self.moves:
                self.pending = self.moves.pop(0)
            else:
                self._finish()
            return

        if self.book:
            self.pending = self.board.parse_san(self.book.pop(0))
            return
        if self.board.is_game_over(claim_draw=True) or self.board.ply() >= MAX_PLIES:
            self._finish()
            return
        import chessbot
        board = self.board.copy()
        def work():
            self.pending = chessbot.choose_move(board, soft_time=0.5, hard_time=1.0)
        threading.Thread(target=work, daemon=True).start()

    def _finish(self):
        outcome = self.board.outcome(claim_draw=True)
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            self.result_text = f"Checkmate - {winner} wins"
        elif outcome is not None and outcome.winner is None:
            self.result_text = outcome.termination.name.replace("_", " ").capitalize() + " - draw"
        elif self.result == "1-0":
            self.result_text = "White wins"
        elif self.result == "0-1":
            self.result_text = "Black wins"
        else:
            self.result_text = "Draw"
        self.over_at = time.time()

    def update(self, now):
        # returns True when the game is over and a new one should start
        if self.over_at is not None:
            return now - self.over_at >= GAME_END_PAUSE
        if self.anim is not None:
            start, move = self.anim
            if now - start >= MOVE_ANIM:
                self.history.append(self.board.san(move))
                self.board.push(move)
                self.last_move = move
                self.anim = None
                self.next_move_at = now + MOVE_PAUSE
                self._think()
        elif self.pending is not None and now >= self.next_move_at:
            self.anim = (now, self.pending)
            self.pending = None
        return False

_game = None
_active = False
_auto = False           # activated by the idle timer (so driving off wakes it)
_level = 0.0            # fade: 0 = hidden, 1 = fully shown
_last_draw = time.time()
_idle_since = None
_swallow_until = 0

def activate(auto=False):
    global _active, _auto, _game
    _auto = auto
    if not _active:
        _game = _Game()
    _active = True

def deactivate():
    global _active, _idle_since, _swallow_until
    _active = False
    _idle_since = time.time()
    _swallow_until = time.time() + 0.3

def _draw_board(scene, game, sq, now):
    board = game.board
    last = set()
    if game.last_move is not None:
        last = {game.last_move.from_square, game.last_move.to_square}

    for square in chess.SQUARES:
        light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        if square in last:
            color = LIGHT_LAST if light else DARK_LAST
        else:
            color = LIGHT_SQUARE if light else DARK_SQUARE
        pygame.draw.rect(scene, color, pygame.Rect(*chessdraw.square_pos(square, sq), sq, sq))

    # pieces that are moving, with where they come from and go to
    hidden = set()
    movers = []
    fading = None
    progress = 0
    if game.anim is not None:
        start, move = game.anim
        progress = min(1.0, (now - start) / MOVE_ANIM)
        progress = progress * progress * (3 - 2 * progress)     # ease in and out
        hidden.add(move.from_square)
        movers.append((board.piece_at(move.from_square), move.from_square, move.to_square))
        if board.is_castling(move):
            rank = chess.square_rank(move.from_square)
            kingside = chess.square_file(move.to_square) > chess.square_file(move.from_square)
            rook_from = chess.square(7 if kingside else 0, rank)
            rook_to = chess.square(5 if kingside else 3, rank)
            hidden.add(rook_from)
            movers.append((board.piece_at(rook_from), rook_from, rook_to))
        if board.is_en_passant(move):
            captured_square = chess.square(chess.square_file(move.to_square), chess.square_rank(move.from_square))
        else:
            captured_square = move.to_square
        captured = board.piece_at(captured_square)
        if captured is not None and not board.is_castling(move):
            hidden.add(captured_square)
            fading = (captured, captured_square)

    for square, piece in board.piece_map().items():
        if square not in hidden:
            scene.blit(chessdraw.piece_surface(piece, sq), chessdraw.square_pos(square, sq))

    if fading is not None:
        surface = chessdraw.piece_surface(fading[0], sq).copy()
        surface.set_alpha(int(255 * (1 - progress)))
        scene.blit(surface, chessdraw.square_pos(fading[1], sq))

    for piece, from_square, to_square in movers:
        x0, y0 = chessdraw.square_pos(from_square, sq)
        x1, y1 = chessdraw.square_pos(to_square, sq)
        scene.blit(chessdraw.piece_surface(piece, sq), (x0 + (x1 - x0) * progress, y0 + (y1 - y0) * progress))

def _fit(text, size, color, max_width):
    # render text, shrinking the font until it fits
    while True:
        surface = chessdraw.font(size).render(text, True, color)
        if surface.get_width() <= max_width or size <= 12:
            return surface
        size -= 2

def _draw_panel(scene, game, x, height, size, max_width):
    title = chessdraw.font(int(size * 0.075)).render("CHESS", True, ACCENT_COLOR)
    scene.blit(title, (x, 0))

    # players, with a chip showing their colour
    chip = int(size * 0.03)
    name_size = int(size * 0.05)
    y = int(size * 0.13)
    for name, color in ((game.white, WHITE_PIECE), (game.black, BLACK_PIECE)):
        pygame.draw.rect(scene, color, pygame.Rect(x, y + chip // 3, chip, chip))
        pygame.draw.rect(scene, TEXT_COLOR, pygame.Rect(x, y + chip // 3, chip, chip), 1)
        text = _fit(name, name_size, TEXT_COLOR, max_width - chip * 2)
        scene.blit(text, (x + chip * 2, y))
        y += int(size * 0.062)
    if game.info:
        scene.blit(_fit(game.info, int(size * 0.037), DIM_TEXT_COLOR, max_width), (x, y + int(size * 0.005)))

    # last few full moves, newest at the bottom
    line_font = chessdraw.font(int(size * 0.05))
    line_height = int(size * 0.06)
    pairs = [game.history[i:i + 2] for i in range(0, len(game.history), 2)]
    first = max(0, len(pairs) - 8)
    y = int(size * 0.37)
    for number in range(first, len(pairs)):
        text = f"{number + 1}.  " + "   ".join(pairs[number])
        color = TEXT_COLOR if number == len(pairs) - 1 else DIM_TEXT_COLOR
        scene.blit(line_font.render(text, True, color), (x, y))
        y += line_height

    if game.result_text:
        result = _fit(game.result_text, int(size * 0.055), ACCENT_COLOR, max_width)
        scene.blit(result, (x, height - result.get_height()))
    elif game.board.is_check():
        check = chessdraw.font(int(size * 0.055)).render("Check!", True, ACCENT_COLOR)
        scene.blit(check, (x, height - check.get_height()))

_scene_cache = {}
def _draw(surface):
    global _level, _last_draw, _game
    now = time.time()
    dt = min(now - _last_draw, 0.1)
    _last_draw = now

    if _active:
        _level = min(1.0, _level + dt / FADE_TIME)
    else:
        _level = max(0.0, _level - dt / FADE_TIME)
    if _level <= 0 or _game is None:
        return

    if _active and _game.update(now):
        _game = _Game()

    width, height = surface.get_size()
    sq = int(min(width * 0.5, height * 0.8) // 8)
    board_size = sq * 8
    panel_x = board_size + int(board_size * 0.08)
    scene_width = min(width - 20, panel_x + int(board_size * 0.62))

    scene = _scene_cache.get((scene_width, board_size))
    if scene is None:
        scene = _scene_cache[(scene_width, board_size)] = pygame.Surface((scene_width, board_size))
    scene.fill(DIM_COLOR)
    _draw_board(scene, _game, sq, now)
    _draw_panel(scene, _game, panel_x, board_size, board_size, scene_width - panel_x - 10)

    # drift slowly so nothing stays on the same pixels
    x = (width - scene_width) / 2 + width * 0.03 * math.sin(now / 19)
    y = (height - board_size) / 2 + height * 0.04 * math.cos(now / 23)

    dim = pygame.Surface((width, height))
    dim.fill(DIM_COLOR)
    dim.set_alpha(int(235 * _level))
    surface.blit(dim, (0, 0))
    scene.set_alpha(int(255 * _level))
    surface.blit(scene, (x, y))

# Every screen ends its frame with pygame.display.flip(), so hooking it draws
# the screensaver on top of whichever screen is showing (on the main thread).
_original_flip = pygame.display.flip
def _flip():
    surface = pygame.display.get_surface()
    if surface is not None:
        _draw(surface)
    _original_flip()
pygame.display.flip = _flip

# Screens read their input with pygame.event.get(), so hook it to wake up on a
# touch (and to restart the idle timer on any touch) and keep a waking touch
# away from the screen underneath.
_TOUCH_EVENTS = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.FINGERDOWN, pygame.FINGERUP)
_ACTIVITY_EVENTS = _TOUCH_EVENTS + (pygame.MOUSEMOTION, pygame.FINGERMOTION)
_original_get = pygame.event.get
def _get(*args, **kwargs):
    global _idle_since
    events = _original_get(*args, **kwargs)
    if not _active and any(event.type in _ACTIVITY_EVENTS for event in events):
        # touching the screen restarts the idle timer
        _idle_since = time.time()
    if not _active and time.time() >= _swallow_until:
        return events
    if _active and any(event.type in _TOUCH_EVENTS for event in events):
        deactivate()
    return [event for event in events if event.type not in _TOUCH_EVENTS]
pygame.event.get = _get

def _watch(get_speed):
    global _idle_since
    while True:
        if get_speed() == 0:
            if _idle_since is None:
                _idle_since = time.time()
            elif not _active and time.time() - _idle_since >= IDLE_TIME:
                activate(auto=True)
        else:
            _idle_since = None
            if _active and _auto:
                deactivate()
        time.sleep(0.2)

def start(get_speed):
    threading.Thread(target=_watch, args=(get_speed,), daemon=True).start()
