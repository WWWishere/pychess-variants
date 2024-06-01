from __future__ import annotations

# -*- coding: utf-8 -*-
from ataxx import ATAXX_FENS
from const import CATEGORIES

import logging
import re
import random

log = logging.getLogger(__name__)

try:
    import pyffish as sf
except ImportError:
    log.error("No pyffish module installed!", exc_info=True)

WHITE, BLACK = 0, 1
FILES = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

log = logging.getLogger(__name__)


def file_of(piece: str, rank: str) -> int:
    """
    Returns the 0-based file of the specified piece in the rank.
    Returns -1 if the piece is not in the rank.
    """
    pos = rank.find(piece)
    if pos >= 0:
        return sum(int(p) if p.isdigit() else 1 for p in rank[:pos])
    else:
        return -1


def modded_variant(variant: str, chess960: bool, initial_fen: str) -> str:
    """Some variants need to be treated differently by pyffish."""
    if not chess960 and variant in ("capablanca", "capahouse") and initial_fen:
        """
        E-file king in a Capablanca/Capahouse variant.
        The game will be treated as an Embassy game for the purpose of castling.
        The king starts on the e-file if it is on the e-file in the starting rank and can castle.
        """
        parts = initial_fen.split()
        ranks = parts[0].split("/")
        if (
            parts[2] != "-"
            and (("K" not in parts[2] and "Q" not in parts[2]) or file_of("K", ranks[7]) == 4)
            and (("k" not in parts[2] and "q" not in parts[2]) or file_of("k", ranks[0]) == 4)
        ):
            return "embassyhouse" if "house" in variant else "embassy"
    return variant


class FairyBoard:
    def __init__(
        self, variant: str, initial_fen="", chess960=False, count_started=0, disabled_fen=""
    ):
        self.variant = modded_variant(variant, chess960, initial_fen)
        self.chess960 = chess960
        self.sfen = False
        self.show_promoted = variant in ("makruk", "makpong", "cambodian")
        self.nnue = initial_fen == ""
        self.initial_fen = (
            initial_fen
            if initial_fen
            else FairyBoard.start_fen(variant, chess960 or variant == "ataxx", disabled_fen)
        )
        self.move_stack: list[str] = []
        self.ply = 0
        self.color = WHITE if self.initial_fen.split()[1] == "w" else BLACK
        self.fen = self.initial_fen
        self.manual_count = count_started != 0
        self.count_started = count_started

        if self.variant == "janggi":
            self.notation = sf.NOTATION_JANGGI
        elif self.variant in CATEGORIES["shogi"]:
            self.notation = sf.NOTATION_SHOGI_HODGES_NUMBER
        elif self.variant in (
            "xiangqi",
            "minixiangqi",
        ):  # XIANGQI_WXF can't handle Manchu banner!
            self.notation = sf.NOTATION_XIANGQI_WXF
        else:
            self.notation = sf.NOTATION_SAN

    @staticmethod
    def start_fen(variant, chess960=False, disabled_fen=""):
        if chess960 or variant in ("paradigm30", "randomized", "rand2", "ordarandom"):
            if chess960 and variant == "paradigm30":
                new_fen = FairyBoard.shuffle_start("paradigm1320")
            else:
                new_fen = FairyBoard.shuffle_start(variant)
            while new_fen == disabled_fen:
                new_fen = FairyBoard.shuffle_start(variant)
            return new_fen
        return sf.start_fen(variant)

    @property
    def initial_sfen(self):
        return sf.get_fen(self.variant, self.initial_fen, [], False, True)

    def push(self, move):
        try:
            # log.debug("move=%s, fen=%s", move, self.fen)
            self.move_stack.append(move)
            self.ply += 1
            self.color = WHITE if self.color == BLACK else BLACK
            self.fen = sf.get_fen(
                self.variant,
                self.fen,
                [move],
                self.chess960,
                self.sfen,
                self.show_promoted,
                self.count_started,
            )
        except Exception:
            self.pop()
            log.error(
                "ERROR: sf.get_fen() failed on %s %s %s %s %s %s %s",
                self.variant,
                self.fen,
                move,
                self.chess960,
                self.sfen,
                self.show_promoted,
                self.count_started,
                exc_info=True,
            )
            raise

    def pop(self):
        self.move_stack.pop()
        self.ply -= 1
        self.color = not self.color
        self.fen = sf.get_fen(
            self.variant,
            self.initial_fen,
            self.move_stack,
            self.chess960,
            self.sfen,
            self.show_promoted,
            self.count_started,
        )

    def get_san(self, move):
        return sf.get_san(self.variant, self.fen, move, self.chess960, self.notation)

    def legal_moves(self):
        # move legality can depend on history, e.g., passing and bikjang
        return sf.legal_moves(self.variant, self.initial_fen, self.move_stack, self.chess960)

    def is_checked(self):
        return sf.gives_check(self.variant, self.fen, [], self.chess960)

    def insufficient_material(self):
        return sf.has_insufficient_material(self.variant, self.fen, [], self.chess960)

    def is_immediate_game_end(self):
        immediate_end, result = sf.is_immediate_game_end(
            self.variant, self.initial_fen, self.move_stack, self.chess960
        )
        return immediate_end, result

    def is_optional_game_end(self):
        return sf.is_optional_game_end(
            self.variant,
            self.initial_fen,
            self.move_stack,
            self.chess960,
            self.count_started,
        )

    def is_claimable_draw(self):
        optional_end, result = self.is_optional_game_end()
        return optional_end and result == 0

    def game_result(self):
        return sf.game_result(self.variant, self.initial_fen, self.move_stack, self.chess960)

    def print_pos(self):
        print()
        uni_pieces = {
            "R": "♜",
            "N": "♞",
            "B": "♝",
            "Q": "♛",
            "K": "♚",
            "P": "♟",
            "r": "♖",
            "n": "♘",
            "b": "♗",
            "q": "♕",
            "k": "♔",
            "p": "♙",
            ".": "·",
            "/": "\n",
        }
        fen = self.fen
        if "[" in fen:
            board, rest = fen.split("[")
        else:
            board = fen.split()[0]
        board = board.replace("+", "")
        board = re.sub(r"\d", (lambda m: "." * int(m.group(0))), board)
        print("", " ".join(uni_pieces.get(p, p) for p in board))

    def janggi_setup(self, color):
        if color == "b":
            left = random.choice(("nb", "bn"))
            right = random.choice(("nb", "bn"))
            fen = "r%sa1a%sr/4k4/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/4K4/RNBA1ABNR w - - 0 1" % (
                left,
                right,
            )
        else:
            left = random.choice(("NB", "BN"))
            right = random.choice(("NB", "BN"))
            parts = self.initial_fen.split("/")
            parts[-1] = "R%sA1A%sR w - - 0 1" % (left, right)
            fen = "/".join(parts)
        print("-------new FEN", fen)
        self.initial_fen = fen
        self.fen = self.initial_fen

    @staticmethod
    def shuffle_start(variant):
        """Create random initial position.
        The king is placed somewhere between the two rooks.
        The bishops are placed on opposite-colored squares.
        Same for queen and archbishop in caparandom."""

        if variant == "ataxx":
            return random.choice(ATAXX_FENS)

        castl = ""
        capa = variant in ("capablanca", "capahouse")
        seirawan = variant in ("seirawan", "shouse")
        para = variant in ("paradigm30", "paradigm1320")
        para1320 = variant == "paradigm1320"
        rand = variant == "randomized"
        rand2 = variant == "rand2"
        rand_o = variant == "ordarandom"

        # https://www.chessvariants.com/contests/10/crc.html
        # we don't skip spositions that have unprotected pawns
        if capa:
            board = [""] * 10
            positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            bright = [1, 3, 5, 7, 9]
            dark = [0, 2, 4, 6, 8]

            # 1. select queen or the archbishop to be placed first
            piece = random.choice("qa")

            # 2. place the selected 1st piece upon a bright square
            piece_pos = random.choice(bright)
            board[piece_pos] = piece
            positions.remove(piece_pos)
            bright.remove(piece_pos)

            # 3. place the selected 2nd piece upon a dark square
            piece_pos = random.choice(dark)
            board[piece_pos] = "q" if piece == "a" else "a"
            positions.remove(piece_pos)
            dark.remove(piece_pos)
        elif rand or rand_o:
            board = [""] * 8
            positions = [0, 1, 2, 3, 5, 6, 7]
            bright = [1, 3, 5, 7]
            dark = [0, 2, 6]
            selection = [""] * 7
            # For random mirror, the pieces are ranked and chosen by rank
        elif rand2:
            board = [""] * 8
            positions = [0, 1, 2, 3, 4, 5, 6, 7]
            bright = [1, 3, 5, 7]
            dark = [0, 2, 4, 6]
            selection = [""] * 8
            dist = [0] * 2
            rk0 = ["p", "s", "e", "t"]
            rk1 = ["n", "g", "w", "o", "y"]
            rk1c = ["b", "v", "f", "l", "j"]
            rk2 = ["r", "d", "h", "i", "u", "x"]
            rk3 = ["q", "a", "c", "m", "z"]
            rk1dist = [1, 1, 2, 3, 3, 4]
            rk2dist = [1, 1, 2]
            dist[0] = random.choice(rk1dist)
            dist[1] = random.choice(rk2dist)
            selection[0] = random.choice(rk0)
            selection[1] = random.choice(rk1c)
            rk1c.remove(selection[1])
            if dist[0] in (2, 3):
                selection[2] = selection[1]
            else:
                selection[2] = random.choice(rk1c)
            selection[3] = random.choice(rk1)
            rk1.remove(selection[3])
            if dist[0] in (3, 4):
                selection[4] = selection[3]
            else:
                selection[4] = random.choice(rk1)
            selection[5] = random.choice(rk2)
            rk2.remove(selection[5])
            if dist[1] == 2:
                selection[6] = selection[5]
            else:
                selection[6] = random.choice(rk2)
            selection[7] = random.choice(rk3)
            # similar piece placement to 960
        else:
            board = [""] * 8
            positions = [0, 1, 2, 3, 4, 5, 6, 7]
            bright = [1, 3, 5, 7]
            dark = [0, 2, 4, 6]
        if para and not para1320:
            positions.remove(0)
            positions.remove(7)
            positions.remove(4)
            bright.remove(7)
            dark.remove(0)
            dark.remove(4)

        # 3.5. generate piece army for randomized mode
        if rand:
            score = 62
            values = [6, 9, 10, 11, 12, 12, 13, 14, 16, 16, 17, 17, 18, 18, 19, 19, 24]
            values_m = [6, 6, 9, 10, 11, 12, 13, 14]
            values_ms = [6, 6, 6, 9, 10, 11, 12, 13]
            values_mss = [6, 6, 6, 6, 9, 9, 10, 10, 11, 12]
            values_sm = [6, 6, 6, 6, 9, 10]
            values_s = [6, 6, 6, 6, 6, 10]
            selection_num = [0] * 7

            def rollonce(score):
                amtLeft = score
                result = [0] * 5
                k = random.choice(values_m)
                result[0] = k
                amtLeft -= k
                if amtLeft <= 24:
                    result[1] = 6
                    result[2] = 6
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 25:
                    result[1] = 9
                    result[2] = 6
                    result[3] = 6
                    result[4] = 4
                elif amtLeft <= 26:
                    result[1] = 10
                    result[2] = 6
                    result[3] = 6
                    result[4] = 4
                elif amtLeft <= 27:
                    result[1] = 9
                    result[2] = 6
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 28:
                    result[1] = 10
                    result[2] = 6
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 29:
                    result[1] = 10
                    result[2] = 9
                    result[3] = 6
                    result[4] = 4
                elif amtLeft <= 30:
                    result[1] = 9
                    result[2] = 9
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 31:
                    result[1] = 10
                    result[2] = 9
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 32:
                    result[1] = 10
                    result[2] = 10
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 33:
                    result[1] = 12
                    result[2] = 9
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 34:
                    result[1] = 12
                    result[2] = 10
                    result[3] = 6
                    result[4] = 6
                else:
                    result[1] = 10
                    result[2] = 10
                    result[3] = 9
                    result[4] = 6
                return result

            def rollhalf(score):
                amtLeft = score
                result = [0] * 5
                k = random.choice(values_m)
                l = random.choice(values_sm)
                result[0] = k
                result[1] = l
                amtLeft -= k
                amtLeft -= l
                if amtLeft <= 18:
                    result[2] = 6
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 19:
                    result[2] = 9
                    result[3] = 6
                    result[4] = 4
                elif amtLeft <= 20:
                    result[2] = 10
                    result[3] = 6
                    result[4] = 4
                elif amtLeft <= 21:
                    result[2] = 9
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 22:
                    result[2] = 10
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 23:
                    result[2] = 11
                    result[3] = 6
                    result[4] = 6
                elif amtLeft <= 24:
                    result[2] = 9
                    result[3] = 9
                    result[4] = 6
                elif amtLeft <= 25:
                    result[2] = 10
                    result[3] = 9
                    result[4] = 6
                elif amtLeft <= 26:
                    result[2] = 10
                    result[3] = 10
                    result[4] = 6
                elif amtLeft <= 27:
                    result[2] = 12
                    result[3] = 9
                    result[4] = 6
                elif amtLeft <= 28:
                    result[2] = 10
                    result[3] = 9
                    result[4] = 9
                elif amtLeft <= 29:
                    result[2] = 10
                    result[3] = 10
                    result[4] = 9
                elif amtLeft <= 30:
                    result[2] = 12
                    result[3] = 12
                    result[4] = 6
                elif amtLeft <= 31:
                    result[2] = 12
                    result[3] = 10
                    result[4] = 9
                elif amtLeft <= 32:
                    result[2] = 12
                    result[3] = 11
                    result[4] = 9
                elif amtLeft <= 33:
                    result[2] = 12
                    result[3] = 11
                    result[4] = 10
                elif amtLeft <= 34:
                    result[2] = 12
                    result[3] = 12
                    result[4] = 10
                else:
                    result[2] = 14
                    result[3] = 12
                    result[4] = 9
                return result

            def rolltwice(score):
                amtLeft = score
                result = [0] * 5
                k = random.choice(values_m)
                l = random.choice(values_mss)
                result[0] = k
                result[1] = l
                amtLeft -= k
                amtLeft -= l
                if amtLeft <= 24:
                    result[2] = 11
                    result[3] = 10
                    result[4] = 6
                elif amtLeft <= 25:
                    result[2] = 10
                    result[3] = 9
                    result[4] = 6
                elif amtLeft <= 26:
                    result[2] = 10
                    result[3] = 10
                    result[4] = 6
                elif amtLeft <= 27:
                    result[2] = 11
                    result[3] = 10
                    result[4] = 6
                elif amtLeft <= 28:
                    result[2] = 13
                    result[3] = 9
                    result[4] = 6
                elif amtLeft <= 29:
                    result[2] = 10
                    result[3] = 10
                    result[4] = 9
                elif amtLeft <= 30:
                    result[2] = 11
                    result[3] = 10
                    result[4] = 9
                elif amtLeft <= 31:
                    result[2] = 12
                    result[3] = 10
                    result[4] = 9
                elif amtLeft <= 32:
                    result[2] = 12
                    result[3] = 10
                    result[4] = 10
                elif amtLeft <= 33:
                    result[2] = 12
                    result[3] = 11
                    result[4] = 10
                elif amtLeft <= 34:
                    result[2] = 12
                    result[3] = 12
                    result[4] = 10
                elif amtLeft <= 35:
                    result[2] = 14
                    result[3] = 12
                    result[4] = 9
                else:
                    result[2] = 14
                    result[3] = 12
                    result[4] = 12
                return result

            i = random.choice(values)
            selection_num[0] = i
            score -= i
            if i == 24:
                j = random.choice(values_s)
            elif i == 19:
                j = random.choice(values_ms)
            else:
                j = random.choice(values_m)
            selection_num[1] = j
            score -= j
            if score <= 28:
                selection_num[2] = 6
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 4
            elif score <= 30:
                selection_num[2] = 6
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 31:
                selection_num[2] = 9
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 4
            elif score <= 32:
                selection_num[2] = 10
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 4
            elif score <= 33:
                selection_num[2] = 9
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 34:
                selection_num[2] = 10
                selection_num[3] = 6
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 35:
                selection_num[2] = 10
                selection_num[3] = 9
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 4
            elif score <= 36:
                selection_num[2] = 9
                selection_num[3] = 9
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 37:
                selection_num[2] = 10
                selection_num[3] = 9
                selection_num[4] = 6
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 41:
                selection_num[2:7] = rollonce(score)
            elif score <= 47:
                selection_num[2:7] = rollhalf(score)
            else:
                selection_num[2:7] = rolltwice(score)
            for m in range(0, 7):
                n = selection_num[m]
                if n == 4:
                    selection[m] = "l"
                elif n == 6:
                    selection[m] = random.choice(("b", "n", "d", "y"))
                elif n == 9:
                    selection[m] = "w"
                elif n == 10:
                    selection[m] = "r"
                elif n == 11:
                    selection[m] = "h"
                elif n == 12:
                    selection[m] = random.choice(("g", "o"))
                elif n == 13:
                    selection[m] = "i"
                elif n == 14:
                    selection[m] = "c"
                elif n == 16:
                    selection[m] = "m"
                elif n == 17:
                    selection[m] = "u"
                elif n == 18:
                    selection[m] = "q"
                elif n == 19:
                    selection[m] = "v"
                elif n == 24:
                    selection[m] = "a"
            random.shuffle(selection)
        elif rand_o:
            score = 66
            selection_num = [0] * 7
            values = [6, 7, 8, 9, 9, 10, 10, 12, 12, 14, 14, 15, 15]
            values_l = [10, 12, 14, 15]
            values_m = [8, 8, 9, 10, 12, 12, 14]
            values_s = [6, 8, 8, 9, 10]
            i = random.choice(values)
            selection_num[0] = i
            score -= i
            # max = 60, min = 51
            if score >= 57:
                j = random.choice(values_l)
            else:
                j = random.choice(values)
            selection_num[1] = j
            score -= j
            # max = 50, min = 36
            if score >= 47:
                k = random.choice(values_l)
            elif score <= 39:
                k = random.choice(values_s)
            else:
                k = random.choice(values_m)
            selection_num[2] = k
            score -= k
            # max = 40, min = 26
            if score >= 35:
                l = random.choice(values_l)
            elif score <= 31:
                l = random.choice(values_s)
            else:
                l = random.choice(values_m)
            selection_num[3] = l
            score -= l
            # max = 30, min = 16
            if score <= 16:
                selection_num[4] = 7
                selection_num[5] = 6
                selection_num[6] = 3
            elif score <= 17:
                selection_num[4] = 8
                selection_num[5] = 6
                selection_num[6] = 3
            elif score <= 18:
                selection_num[4] = 9
                selection_num[5] = 6
                selection_num[6] = 3
            elif score <= 19:
                selection_num[4] = 7
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 20:
                selection_num[4] = 8
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 21:
                selection_num[4] = 9
                selection_num[5] = 6
                selection_num[6] = 6
            elif score <= 22:
                selection_num[4] = 9
                selection_num[5] = 7
                selection_num[6] = 6
            elif score <= 23:
                selection_num[4] = 10
                selection_num[5] = 7
                selection_num[6] = 6
            elif score <= 24:
                selection_num[4] = 9
                selection_num[5] = 9
                selection_num[6] = 6
            elif score <= 25:
                selection_num[4] = 10
                selection_num[5] = 9
                selection_num[6] = 6
            elif score <= 26:
                selection_num[4] = 12
                selection_num[5] = 8
                selection_num[6] = 6
            elif score <= 27:
                selection_num[4] = 14
                selection_num[5] = 7
                selection_num[6] = 6
            elif score <= 28:
                selection_num[4] = 10
                selection_num[5] = 9
                selection_num[6] = 9
            elif score <= 29:
                selection_num[4] = 12
                selection_num[5] = 10
                selection_num[6] = 7
            elif score <= 30:
                selection_num[4] = 14
                selection_num[5] = 10
                selection_num[6] = 6
            for m in range(0, 7):
                n = selection_num[m]
                if n == 3:
                    selection[m] = "y"
                elif n == 6:
                    selection[m] = random.choice(("t", "g", "n"))
                elif n == 7:
                    selection[m] = "v"
                elif n == 8:
                    selection[m] = random.choice(("a", "l", "d", "s"))
                elif n == 9:
                    selection[m] = random.choice(("w", "x"))
                elif n == 10:
                    selection[m] = random.choice(("f", "z"))
                elif n == 12:
                    selection[m] = "h"
                elif n == 14:
                    selection[m] = "c"
                else:
                    selection[m] = random.choice(("i", "o"))
            random.shuffle(selection)

        # 4. one bishop has to be placed upon a bright square
        # 4.5 without colorbound restrictions, bishop color separation is not needed
        else:
            piece_pos = random.choice(bright)
            if para1320:
                piece_pos = random.choice(positions)
            if para:
                board[piece_pos] = "d"
            elif rand2:
                board[piece_pos] = selection[1]
            else:
                board[piece_pos] = "b"
            positions.remove(piece_pos)
            if seirawan:
                castl += FILES[piece_pos]

            # 5. one bishop has to be placed upon a dark square
            # 5.5 one bishop is placed on any square
            piece_pos = random.choice(dark)
            if para1320:
                piece_pos = random.choice(positions)
            if para:
                board[piece_pos] = "d"
            elif rand2:
                board[piece_pos] = selection[2]
            else:
                board[piece_pos] = "b"
            positions.remove(piece_pos)
            if seirawan:
                castl += FILES[piece_pos]

            if capa:
                # 6. one chancellor has to be placed upon a free square
                piece_pos = random.choice(positions)
                board[piece_pos] = "c"
                positions.remove(piece_pos)
            elif rand2:
                piece_pos = random.choice(positions)
                board[piece_pos] = selection[7]
                positions.remove(piece_pos)
            else:
                piece_pos = random.choice(positions)
                board[piece_pos] = "q"
                positions.remove(piece_pos)
                if seirawan:
                    castl += FILES[piece_pos]

            # 7. one knight has to be placed upon a free square
            piece_pos = random.choice(positions)
            if rand2:
                board[piece_pos] = selection[3]
            else:
                board[piece_pos] = "n"
            positions.remove(piece_pos)
            if seirawan:
                castl += FILES[piece_pos]

            # 8. one knight has to be placed upon a free square
            piece_pos = random.choice(positions)
            if rand2:
                board[piece_pos] = selection[4]
            else:
                board[piece_pos] = "n"
            positions.remove(piece_pos)
            if seirawan:
                castl += FILES[piece_pos]

            # 9. set the king upon the center of three free squares left
            if para and not para1320:
                positions = [0,4,7]
            piece_pos = positions[1]
            board[piece_pos] = "k"

            # 10. set the rooks upon the both last free squares left
            piece_pos = positions[0]
            if rand2:
                board[piece_pos] = selection[5]
            else:
                board[piece_pos] = "r"
            castl += "q" if seirawan or para else FILES[piece_pos]

            piece_pos = positions[2]
            if rand2:
                board[piece_pos] = selection[6]
            else:
                board[piece_pos] = "r"
            castl += "k" if seirawan or para else FILES[piece_pos]

        # 11. overwrite board randomization in randomized
        if rand or rand_o:
            board[0:4] = selection[0:4]
            board[4] = "k"
            board[5:8] = selection[4:7]

        fen = "".join(board)
        if capa:
            body = "/pppppppppp/10/10/10/10/PPPPPPPPPP/"
        elif rand:
            body = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/"
        elif rand_o:
            body = "lhafkahl/8/pppppppp/8/8/PPPPPPPP/8/"
        elif rand2:
            pawns = selection[0] * 8
            pawnsUp = pawns.upper()
            body = "/" + pawns + "/8/8/8/8/" + pawnsUp + "/"
        else:
            body = "/pppppppp/8/8/8/8/PPPPPPPP/"

        if variant in ("crazyhouse", "capahouse"):
            holdings = "[]"
        elif seirawan:
            holdings = "[HEhe]"
        else:
            holdings = ""

        checks = "3+3 " if variant == "3check" else ""

        if rand:
            fen = (
                body
                + fen.upper()
                + " w "
                + "kq"
                + " - "
                + checks
                + "0 1"
            )
        elif rand_o:
            fen = (
                body
                + fen.upper()
                + " w "
                + "-"
                + " - "
                + checks
                + "0 1"
            )

        else:
            fen = (
                fen
                + body
                + fen.upper()
                + holdings
                + " w "
                + castl.upper()
                + castl
                + " - "
                + checks
                + "0 1"
            )
        return fen


if __name__ == "__main__":
    sf.set_option("VariantPath", "variants.ini")

    board = FairyBoard("shogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("placement")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("makruk")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("sittuyin")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("capablanca")
    print(board.fen)
    for move in (
        "e2e4",
        "d7d5",
        "e4d5",
        "c8i2",
        "d5d6",
        "i2j1",
        "d6d7",
        "j1e6",
        "d7e8c",
    ):
        print("push move", move)
        board.push(move)
        board.print_pos()
        print(board.fen)
    print(board.legal_moves())

    FEN = "r8r/1nbqkcabn1/ppppppp1pp/10/9P/10/10/PPPPPPPPp1/1NBQKC2N1/R5RAB1[p] b - - 0 5"
    board = FairyBoard("grandhouse", initial_fen=FEN)
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("minishogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("kyotoshogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    print("--- SHOGUN ---")
    print(FairyBoard.start_fen("shogun"))
    board = FairyBoard("shogun")
    for move in ("c2c4", "b8c6", "b2b4", "b7b5", "c4b5", "c6b8"):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    FEN = "rnb+fkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB+FKBNR w KQkq - 0 1"
    board = FairyBoard("shogun", initial_fen=FEN)
    for move in (
        "c2c4",
        "h7h6",
        "c4c5",
        "h6h5",
        "c5c6+",
        "h8h6",
        "c6b7",
        "g7g6",
        "b7a8",
        "c8a6",
        "a8b7",
        "b8c6",
        "d1b3",
        "a6e2+",
        "b3b6",
        "e7e6",
        "b6c7",
        "P@h4",
        "c7c8",
        "e2c4",
        "f1c4",
        "h6h8",
        "c4e6+",
        "g8h6",
        "b2b4",
        "h8g8",
        "b4b5",
        "g6g5",
        "b5c6",
        "f8e7",
        "c6c7",
        "d7e6",
        "c8b8",
        "B@b6",
    ):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    board = FairyBoard("shouse")
    for move in (
        "e2e4",
        "E@d4",
        "g1f3",
        "e7e6",
        "b1c3",
        "H@b6",
        "d2d3",
        "f8b4",
        "c1e3",
        "d4b5",
        "e3b6",
        "a7b6",
        "d1d2e",
        "B@c6",
        "f1e2",
        "b5h5",
    ):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    board = FairyBoard("empire")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())
    print([board.get_san(move) for move in board.legal_moves()])

    board = FairyBoard("ordamirror")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())
    print([board.get_san(move) for move in board.legal_moves()])

    print(sf.version())
    print(sf.info())
    print(sf.variants())
