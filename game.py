import random

from enum import Enum


class Game():

    def __init__(self):
        self.board = Board()

    def play(self):
        while True:
            self.board.print_board()
            new_piece = self._random_piece()
            # generate a random piece
            # player gets the place the piece
            # print the board
            # randomly cause avalanches

    def _random_piece(self):
        piece_type = random.choice(PieceType.__members__)
        return Piece(piece_type)


class Board():

    def __init__(self, width=20, height=40):
        self._board_matrix = self.make_initial_board(width, height)

    def make_initial_board(self, width, height):
        return [[None for _ in range(width)] for _ in range(height)]

    def print_board(self):
        print(*self._board_matrix, sep='\n')

    def add_piece(self, row, column, piecetype):
        self._board_matrix[column][row] = Piece(piecetype)


class PieceType(Enum):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'
    GRAY = 'gray'


class Piece():

    def __init__(self, input_type):
        self.type = PieceType(input_type)

    def __repr__(self):
        return str(self.type)


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
