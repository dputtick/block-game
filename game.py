from enum import Enum


class Board():
    def __init__(self, width=10, height=20):
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
    board = Board()
    board.add_piece(1, 1, 'red')
    board.print_board()


if __name__ == '__main__':
    main()
