import chess
import pygame

# Shared chess drawing: colours, fonts and piece images used by the
# screensaver and the chess game.

LIGHT_SQUARE = (118, 124, 140)
DARK_SQUARE = (58, 62, 76)
LIGHT_LAST = (160, 160, 110)
DARK_LAST = (110, 110, 60)
WHITE_PIECE = (238, 238, 242)
BLACK_PIECE = (24, 24, 30)
TEXT_COLOR = (170, 170, 182)
DIM_TEXT_COLOR = (105, 105, 118)
ACCENT_COLOR = (255, 190, 60)

_font_cache = {}
def font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]

_glyph_font_path = None
_glyph_font_checked = False
def glyph_font(size):
    # a font that has the chess symbols (DejaVu Sans on most systems), or None
    global _glyph_font_path, _glyph_font_checked
    if not _glyph_font_checked:
        _glyph_font_checked = True
        path = pygame.font.match_font("dejavusans,freeserif,symbola,notosanssymbols2,segoeuisymbol")
        if path and pygame.font.Font(path, 20).metrics("♚")[0] is not None:
            _glyph_font_path = path
    if _glyph_font_path is None:
        return None
    key = ("glyph", size)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.Font(_glyph_font_path, size)
    return _font_cache[key]

_GLYPHS = {chess.KING: "♚", chess.QUEEN: "♛", chess.ROOK: "♜",
           chess.BISHOP: "♝", chess.KNIGHT: "♞", chess.PAWN: "♟"}

_piece_cache = {}
def piece_surface(piece, size):
    key = (piece.piece_type, piece.color, size)
    if key in _piece_cache:
        return _piece_cache[key]

    color = WHITE_PIECE if piece.color else BLACK_PIECE
    outline = BLACK_PIECE if piece.color else WHITE_PIECE
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    symbols = glyph_font(int(size * 0.9))
    if symbols is not None:
        glyph = _GLYPHS[piece.piece_type]
        center = (size // 2, size // 2)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            shadow = symbols.render(glyph, True, outline)
            surface.blit(shadow, shadow.get_rect(center=(center[0] + dx, center[1] + dy)))
        text = symbols.render(glyph, True, color)
        surface.blit(text, text.get_rect(center=center))
    else:
        # no symbol font: a disc with the piece letter
        pygame.draw.circle(surface, color, (size // 2, size // 2), int(size * 0.38))
        pygame.draw.circle(surface, outline, (size // 2, size // 2), int(size * 0.38), 2)
        text = font(int(size * 0.5)).render(piece.symbol().upper(), True, outline)
        surface.blit(text, text.get_rect(center=(size // 2, size // 2)))

    _piece_cache[key] = surface
    return surface

def square_pos(square, sq, white_bottom=True):
    # top left of a square, the player's side at the bottom
    file, rank = chess.square_file(square), chess.square_rank(square)
    if white_bottom:
        return (file * sq, (7 - rank) * sq)
    return ((7 - file) * sq, rank * sq)
