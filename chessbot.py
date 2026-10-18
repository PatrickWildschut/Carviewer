import random
import time
import chess

# A chess bot. It searches deeper and deeper (iterative deepening, alpha-beta)
# and plays the best move it has found. To keep games varied it picks randomly
# among the moves that are within RANDOMNESS centipawns of the best one.
#
# It thinks for about SOFT_TIME seconds. If the position still looks unsettled
# at that point (the best move just changed, or the score dropped) it keeps
# going, but never longer than HARD_TIME. A calm position uses less CPU, a
# tactical one gets the extra time.
# Usage: move = choose_move(board)

SOFT_TIME = 1.0
HARD_TIME = 5.0
MAX_DEPTH = 8
RANDOMNESS = 15     # centipawns (100 = one pawn); 0 = always the single best move

# Opening lines, picked at random by the screensaver's fallback mode
OPENINGS = {
    "Italian Game": "e4 e5 Nf3 Nc6 Bc4 Bc5",
    "London System": "d4 d5 Nf3 Nf6 Bf4 e6",
    "Stafford Gambit": "e4 e5 Nf3 Nf6 Nxe5 Nc6 Nxc6 dxc6",
}

PIECE_VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
MATE_SCORE = 100000
MAX_TABLE_SIZE = 300000

# Piece square tables (from white's point of view, a8 first, like a board
# printed from above). Based on the "simplified evaluation function".
_PAWN = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0]
_KNIGHT = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]
_BISHOP = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]
_ROOK = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0]
_QUEEN = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]
_KING_MIDDLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20]
_KING_END = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50]

def _table_for(table, color):
    # index by python-chess square (a1 = 0) for the given colour
    if color == chess.WHITE:
        return [table[(7 - chess.square_rank(sq)) * 8 + chess.square_file(sq)] for sq in chess.SQUARES]
    return [table[chess.square_rank(sq) * 8 + chess.square_file(sq)] for sq in chess.SQUARES]

_TABLES = {
    chess.PAWN: _PAWN, chess.KNIGHT: _KNIGHT, chess.BISHOP: _BISHOP,
    chess.ROOK: _ROOK, chess.QUEEN: _QUEEN,
}
PST = {(piece_type, color): _table_for(table, color)
       for piece_type, table in _TABLES.items() for color in chess.COLORS}
KING_MIDDLE = {color: _table_for(_KING_MIDDLE, color) for color in chess.COLORS}
KING_END = {color: _table_for(_KING_END, color) for color in chess.COLORS}

def evaluate(board):
    # centipawns from the point of view of the side to move
    pieces = board.piece_map()
    if len(pieces) <= 4 and board.is_insufficient_material():
        return 0

    score = {chess.WHITE: 0, chess.BLACK: 0}
    queens = 0
    material = 0
    for square, piece in pieces.items():
        if piece.piece_type == chess.KING:
            continue
        score[piece.color] += PIECE_VALUES[piece.piece_type] + PST[(piece.piece_type, piece.color)][square]
        if piece.piece_type == chess.QUEEN:
            queens += 1
        if piece.piece_type != chess.PAWN:
            material += PIECE_VALUES[piece.piece_type]

    endgame = queens == 0 or material <= 2600
    kings = KING_END if endgame else KING_MIDDLE
    for color in chess.COLORS:
        king = board.king(color)
        if king is not None:
            score[color] += kings[color][king]

    diff = score[chess.WHITE] - score[chess.BLACK]

    # when far ahead in an endgame, drive the enemy king to the edge and bring
    # our own king closer, otherwise it never finds the mate
    if endgame and abs(diff) > 300:
        winner = chess.WHITE if diff > 0 else chess.BLACK
        winning_king, losing_king = board.king(winner), board.king(not winner)
        if winning_king is not None and losing_king is not None:
            edge = max(3 - min(chess.square_file(losing_king), 7 - chess.square_file(losing_king)), 0) + \
                   max(3 - min(chess.square_rank(losing_king), 7 - chess.square_rank(losing_king)), 0)
            nearness = 14 - (abs(chess.square_file(winning_king) - chess.square_file(losing_king)) +
                             abs(chess.square_rank(winning_king) - chess.square_rank(losing_king)))
            bonus = 10 * edge + 4 * nearness
            diff += bonus if winner == chess.WHITE else -bonus

    return diff if board.turn == chess.WHITE else -diff

class _Timeout(Exception):
    pass

class _Search:
    def __init__(self, board, deadline):
        self.board = board
        self.deadline = deadline
        self.nodes = 0
        self.table = {}     # position -> (depth, kind, score, move)

    def check_time(self):
        self.nodes += 1
        if self.nodes % 256 == 0 and time.time() > self.deadline:
            raise _Timeout()

    def order(self, moves, first=None):
        board = self.board
        def key(move):
            if move == first:
                return 10000
            score = 0
            if board.is_capture(move):
                victim = chess.PAWN if board.is_en_passant(move) else board.piece_type_at(move.to_square)
                score = 10 * PIECE_VALUES[victim] - PIECE_VALUES[board.piece_type_at(move.from_square)] + 1000
            if move.promotion:
                score += PIECE_VALUES[move.promotion]
            return score
        return sorted(moves, key=key, reverse=True)

    def quiesce(self, alpha, beta):
        self.check_time()
        stand_pat = evaluate(self.board)
        if stand_pat >= beta:
            return stand_pat
        alpha = max(alpha, stand_pat)
        for move in self.order(self.board.generate_legal_captures()):
            self.board.push(move)
            score = -self.quiesce(-beta, -alpha)
            self.board.pop()
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return alpha

    def negamax(self, depth, alpha, beta, ply):
        self.check_time()
        board = self.board
        if board.halfmove_clock >= 4 and (board.is_repetition(2) or board.halfmove_clock >= 100):
            return 0

        key = board._transposition_key()
        entry = self.table.get(key)
        table_move = None
        if entry is not None:
            entry_depth, kind, score, table_move = entry
            if score > MATE_SCORE - 1000:
                score -= ply
            elif score < -MATE_SCORE + 1000:
                score += ply
            if entry_depth >= depth:
                if kind == "exact":
                    return score
                if kind == "lower" and score >= beta:
                    return score
                if kind == "upper" and score <= alpha:
                    return score

        if depth <= 0:
            return self.quiesce(alpha, beta)

        moves = list(board.legal_moves)
        if not moves:
            return -MATE_SCORE + ply if board.is_check() else 0

        original_alpha = alpha
        best_score, best_move = -MATE_SCORE * 2, None
        for move in self.order(moves, table_move):
            board.push(move)
            score = -self.negamax(depth - 1, -beta, -alpha, ply + 1)
            board.pop()
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        kind = "exact"
        if best_score <= original_alpha:
            kind = "upper"
        elif best_score >= beta:
            kind = "lower"
        stored = best_score
        if stored > MATE_SCORE - 1000:
            stored += ply
        elif stored < -MATE_SCORE + 1000:
            stored -= ply
        if len(self.table) < MAX_TABLE_SIZE:
            self.table[key] = (depth, kind, stored, best_move)
        return best_score

    def root(self, depth, previous_best):
        # The window stays RANDOMNESS wide below the best score, so every move
        # that is nearly as good as the best gets an exact score too.
        alpha, beta = -MATE_SCORE * 2, MATE_SCORE * 2
        best_score, best_move = -MATE_SCORE * 2, None
        scored = []
        for move in self.order(list(self.board.legal_moves), previous_best):
            self.board.push(move)
            score = -self.negamax(depth - 1, -beta, -alpha, 1)
            self.board.pop()
            scored.append((move, score))
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, best_score - RANDOMNESS)
        if best_score > MATE_SCORE - 1000:
            return best_move, best_score, [best_move]       # never play down a forced mate
        return best_move, best_score, [move for move, score in scored if score > best_score - RANDOMNESS]

def choose_move(board, soft_time=SOFT_TIME, hard_time=HARD_TIME):
    moves = list(board.legal_moves)
    if len(moves) <= 1:
        return moves[0] if moves else None

    start = time.time()
    search = _Search(board.copy(), start + hard_time)
    best_move, best_score = moves[0], None
    candidates = [best_move]
    extend = False          # keep thinking past soft_time, up to hard_time
    depth = 1
    while depth <= MAX_DEPTH:
        # a deeper search that would run past the soft limit is cut off, unless
        # the position is unsettled
        search.deadline = start + (hard_time if extend else soft_time)
        try:
            move, score, candidates_now = search.root(depth, best_move)
        except _Timeout:
            break
        candidates = candidates_now
        unsettled = best_score is not None and (score < best_score - 50 or (move != best_move and abs(score - best_score) > 30))
        best_move, best_score = move, score
        if abs(score) > MATE_SCORE - 1000:
            break                       # found a forced mate
        elapsed = time.time() - start
        extend = unsettled and elapsed >= soft_time / 2
        if elapsed >= soft_time and not extend:
            break                       # calm position, no need to think longer
        depth += 1
    return random.choice(candidates)
