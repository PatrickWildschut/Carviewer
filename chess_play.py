import random
import threading
import time
import chess
import pygame

from Carviewer_Arduino import *
import chessbot
import chessdraw
from chessdraw import (LIGHT_SQUARE, DARK_SQUARE, LIGHT_LAST, DARK_LAST, TEXT_COLOR,
                       DIM_TEXT_COLOR, ACCENT_COLOR)

# Play chess against the bot. Drag a piece to move it (or tap the piece and then
# the square). The colour you play is picked at random for every game.
SQ = S(60)
BOARD_X, BOARD_Y = S(60), S(48)
PANEL_X = BOARD_X + 8 * SQ + S(40)
BOT_MIN_THINK = 1.0     # seconds, so the bot never replies instantly

SELECTED_COLOR = (130, 160, 200)
CHECK_COLOR = (170, 60, 60)
HINT_COLOR = (20, 20, 25)
PROMOTION_PIECES = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]

new_game_button = pygame.Rect(PANEL_X, S(500), S(180), S(50))
back_button = pygame.Rect(PANEL_X + S(200), S(500), S(180), S(50))

class _Play:
    def __init__(self):
        self.board = chess.Board()
        self.player = random.choice([chess.WHITE, chess.BLACK])
        self.history = []
        self.last_move = None
        self.selected = None            # square of the picked up piece
        self.drag_pos = None            # mouse position while dragging
        self.dragging = False
        self.promotion = None           # (from, to) while choosing a promotion piece
        self.bot_move = None
        self.bot_ready_at = 0
        self.result_text = ""
        self.bot_turn_check()

    # ---- turns ----
    def bot_turn_check(self):
        # start the bot thinking when it is its turn
        if self.board.is_game_over(claim_draw=True):
            self.finish()
        elif self.board.turn != self.player:
            board = self.board.copy()
            self.bot_ready_at = time.time() + BOT_MIN_THINK
            def work():
                self.bot_move = chessbot.choose_move(board)
            threading.Thread(target=work, daemon=True).start()

    def finish(self):
        outcome = self.board.outcome(claim_draw=True)
        if self.board.is_checkmate():
            self.result_text = "Checkmate - " + ("you win!" if self.board.turn != self.player else "bot wins")
        elif outcome is not None:
            self.result_text = outcome.termination.name.replace("_", " ").capitalize() + " - draw"
        else:
            self.result_text = "Draw"

    def play(self, move):
        self.history.append(self.board.san(move))
        self.board.push(move)
        self.last_move = move
        self.selected = None
        self.bot_turn_check()

    def update(self):
        if self.bot_move is not None and time.time() >= self.bot_ready_at and not self.result_text:
            move, self.bot_move = self.bot_move, None
            self.play(move)

    def my_turn(self):
        return not self.result_text and self.board.turn == self.player

    # ---- input ----
    def square_at(self, pos):
        x, y = (pos[0] - BOARD_X) // SQ, (pos[1] - BOARD_Y) // SQ
        if not (0 <= x < 8 and 0 <= y < 8):
            return None
        white_bottom = self.player == chess.WHITE
        return chess.square(x if white_bottom else 7 - x, 7 - y if white_bottom else y)

    def targets(self, square):
        return {move.to_square for move in self.board.legal_moves if move.from_square == square}

    def try_move(self, from_square, to_square):
        moves = [m for m in self.board.legal_moves if m.from_square == from_square and m.to_square == to_square]
        if not moves:
            return False
        if len(moves) > 1:
            self.promotion = (from_square, to_square)    # choose queen, rook, bishop or knight
            self.selected = None
        else:
            self.play(moves[0])
        return True

    def promotion_rects(self):
        width = len(PROMOTION_PIECES) * SQ
        x = BOARD_X + (8 * SQ - width) // 2
        y = BOARD_Y + 4 * SQ - SQ // 2
        return [pygame.Rect(x + i * SQ, y, SQ, SQ) for i in range(len(PROMOTION_PIECES))]

    def mouse_down(self, pos):
        if self.promotion is not None:
            for piece_type, rect in zip(PROMOTION_PIECES, self.promotion_rects()):
                if rect.collidepoint(pos):
                    self.play(chess.Move(*self.promotion, promotion=piece_type))
                    break
            self.promotion = None
            return
        if not self.my_turn():
            return
        square = self.square_at(pos)
        if square is None:
            self.selected = None
            return
        if self.selected is not None and square in self.targets(self.selected):
            self.try_move(self.selected, square)        # tap piece, then tap destination
            return
        piece = self.board.piece_at(square)
        if piece is not None and piece.color == self.player:
            self.selected = square
            self.dragging = True
            self.drag_pos = pos
        else:
            self.selected = None

    def mouse_move(self, pos):
        if self.dragging:
            self.drag_pos = pos

    def mouse_up(self, pos):
        if not self.dragging:
            return
        self.dragging = False
        square = self.square_at(pos)
        if square is not None and square != self.selected:
            if not self.try_move(self.selected, square):
                self.selected = None            # dropped on an illegal square
        # dropped back on its own square: stays selected, so a tap works too

    # ---- drawing ----
    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        white_bottom = self.player == chess.WHITE
        last = set()
        if self.last_move is not None:
            last = {self.last_move.from_square, self.last_move.to_square}
        king_in_check = self.board.king(self.board.turn) if self.board.is_check() else None
        targets = self.targets(self.selected) if self.selected is not None else set()

        for square in chess.SQUARES:
            light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
            if square == self.selected:
                color = SELECTED_COLOR
            elif square == king_in_check:
                color = CHECK_COLOR
            elif square in last:
                color = LIGHT_LAST if light else DARK_LAST
            else:
                color = LIGHT_SQUARE if light else DARK_SQUARE
            x, y = chessdraw.square_pos(square, SQ, white_bottom)
            rect = pygame.Rect(BOARD_X + x, BOARD_Y + y, SQ, SQ)
            pygame.draw.rect(screen, color, rect)

            if square in targets:
                if self.board.piece_at(square) is not None:
                    pygame.draw.circle(screen, HINT_COLOR, rect.center, SQ // 2 - S(4), S(4))
                else:
                    pygame.draw.circle(screen, HINT_COLOR, rect.center, SQ // 6)

        for square, piece in self.board.piece_map().items():
            if self.dragging and square == self.selected:
                continue
            x, y = chessdraw.square_pos(square, SQ, white_bottom)
            screen.blit(chessdraw.piece_surface(piece, SQ), (BOARD_X + x, BOARD_Y + y))

        # file letters and rank numbers
        label_font = chessdraw.font(S(20))
        for i in range(8):
            file_letter = "abcdefgh"[i if white_bottom else 7 - i]
            rank_number = str(8 - i if white_bottom else i + 1)
            letter = label_font.render(file_letter, True, DIM_TEXT_COLOR)
            screen.blit(letter, letter.get_rect(center=(BOARD_X + i * SQ + SQ // 2, BOARD_Y + 8 * SQ + S(12))))
            number = label_font.render(rank_number, True, DIM_TEXT_COLOR)
            screen.blit(number, number.get_rect(center=(BOARD_X - S(14), BOARD_Y + i * SQ + SQ // 2)))

        # the piece in hand, under the finger
        if self.dragging and self.selected is not None:
            piece = self.board.piece_at(self.selected)
            screen.blit(chessdraw.piece_surface(piece, SQ), chessdraw.piece_surface(piece, SQ).get_rect(center=self.drag_pos))

        if self.promotion is not None:
            self.draw_promotion()
        self.draw_panel()

    def draw_promotion(self):
        rects = self.promotion_rects()
        backdrop = rects[0].unionall(rects[1:]).inflate(S(20), S(20))
        pygame.draw.rect(screen, BACKGROUND_COLOR, backdrop, border_radius=S(10))
        pygame.draw.rect(screen, ACCENT_COLOR, backdrop, S(2), border_radius=S(10))
        for piece_type, rect in zip(PROMOTION_PIECES, rects):
            pygame.draw.rect(screen, LIGHT_SQUARE, rect.inflate(-S(4), -S(4)))
            screen.blit(chessdraw.piece_surface(chess.Piece(piece_type, self.player), SQ), rect)

    def draw_panel(self):
        title = font_large.render("Chess", True, ACCENT_COLOR)
        screen.blit(title, (PANEL_X, S(50)))

        side = "White" if self.player == chess.WHITE else "Black"
        screen.blit(font_small.render(f"You play {side}", True, TEXT_COLOR), (PANEL_X, S(105)))

        if self.result_text:
            status, color = self.result_text, ACCENT_COLOR
        elif self.promotion is not None:
            status, color = "Promote to...", ACCENT_COLOR
        elif self.board.turn != self.player:
            status, color = "Bot is thinking...", DIM_TEXT_COLOR
        elif self.board.is_check():
            status, color = "Check! Your move", ACCENT_COLOR
        else:
            status, color = "Your move", TEXT_COLOR
        screen.blit(font_small.render(status, True, color), (PANEL_X, S(145)))

        # last few full moves, newest at the bottom
        line_font = chessdraw.font(S(30))
        pairs = [self.history[i:i + 2] for i in range(0, len(self.history), 2)]
        y = S(200)
        for number in range(max(0, len(pairs) - 7), len(pairs)):
            text = f"{number + 1}.  " + "   ".join(pairs[number])
            screen.blit(line_font.render(text, True, TEXT_COLOR if number == len(pairs) - 1 else DIM_TEXT_COLOR), (PANEL_X, y))
            y += S(34)

        for rect, label in ((new_game_button, "New Game"), (back_button, "Back")):
            pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=S(10))
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

def chess_screen():
    clock = pygame.time.Clock()
    game = _Play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return
                elif new_game_button.collidepoint(event.pos):
                    game = _Play()
                else:
                    game.mouse_down(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_move(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game.mouse_up(event.pos)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    chess_screen()
