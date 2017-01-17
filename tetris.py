from utils import Pixel
import random
import time


class Block(object):
    INIT_STEPS = []

    def __init__(self, start):
        self.pixels = []
        self.start = start  # pt tuple
        self.initiate()

    def initiate(self):
        # add additional pixels based on diff from start
        for step in self.INIT_STEPS:
            point = Pixel(*self.start)
            point.step(step)
            self.pixels.append(
                point
            )

    def step(self, direction):
        for p in self.pixels:
            p.step(direction)

    @property
    def all_pixels(self):
        return [p.as_t for p in self.pixels]

    @property
    def pixels_below(self):
        mapped_pixels = []
        for pixel in self.pixels:
            p = Pixel(*pixel.as_t)
            p.step(Pixel.DOWN)
            if p.as_t not in self.all_pixels:
                mapped_pixels.append(p)

        return mapped_pixels


class Triangle(Block):
    """  0
        000
    """
    INIT_STEPS = (1, 0), (0, 1), (1, 1), (2, 1)


class CornerLeft(Block):
    """ 0
        000
    """
    INIT_STEPS = (0, 0), (0, 1), (1, 1), (2, 1)


class CornerRight(Block):
    """   0
        000
    """
    INIT_STEPS = (1, 0), (2, 0), (2, 1), (2, 0)


class LongPiece(Block):
    """
        0000
    """
    INIT_STEPS = (0, 0), (1, 0), (2, 0), (3, 0)


class StepLeft(Block):
    """  00
        00
    """
    INIT_STEPS = (0, 1), (1, 0), (1, 1), (2, 0)


class StepRight(Block):
    """ 00
         00
    """
    INIT_STEPS = (0, 0), (1, 0), (1, 1), (2, 1)


class Square(Block):
    """ 00
        00
    """
    INIT_STEPS = (0, 0), (0, 1), (1, 1), (1, 0)


class TetrisPieces(object):
    START = (2, 0)
    ALL_PIECES = (
        Triangle, CornerLeft, CornerRight,
        LongPiece, StepLeft, StepRight,
        Square
    )

    def __init__(self):
        pass

    def get_random_piece(self):
        piece = random.choice(self.ALL_PIECES)
        return piece(self.START)

    @staticmethod
    def piece_is_stationary(piece, pieces):
        if any(p.y >= 8 for p in piece.pixels_below):
            return True

        all_pixels = []
        for p in pieces:
            if p is not piece:
                all_pixels.extend(p.all_pixels)
        for p in piece.pixels_below:
            if p.as_t in all_pixels:
                return True

        return False


class Tetris(object):
    ROWS = 8
    COLUMNS = 7

    SPEED = 1
    KEYS = {
        'w': Pixel.RIGHT,
        'a': Pixel.DOWN,
        's': Pixel.LEFT,
        'd': Pixel.UP
    }

    def __init__(self):
        self.pieces = []
        self.tp = TetrisPieces()

    def increment(self):
        for piece in self.pieces:
            if not TetrisPieces.piece_is_stationary(piece, self.pieces):
                piece.step(Pixel.DOWN)

    def pretty_print(self):
        matrix = [
            ['0' for x in range(8)]
            for y in range(8)
        ]
        for piece in self.pieces:
            for pixel in piece.pixels:
                matrix[pixel.y][pixel.x] = '1'

        for row in matrix:
            print ''.join(row)

    def game_loop(self):
        while True:
            if not len(self.pieces) or \
                all(TetrisPieces.piece_is_stationary(piece, self.pieces)
                    for piece in self.pieces):
                self.pieces.append(self.tp.get_random_piece())

            self.increment()
            self.pretty_print()
            time.sleep(1)







