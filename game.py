import random

from enum import Enum


class Game():

    def __init__(self):
        self.board = Board()

    def play(self):
        while True:
            self.board.print_board()
            new_piece = self._random_piece()
            row, column = self._get_player_move()
            self.board.add_piece(row, column, new_piece)
            self.board.print_board()
            # randomly cause avalanches

    def _random_piece(self):
        piece_type = random.choice(list(PieceType.__members__.values()))
        return Piece(piece_type)

    def _get_player_move(self):
        row = input("Enter the row you'd like to place your piece in:\n")
        column = input("Column?\n")
        return int(row), int(column)


class Board():

    def __init__(self, width=20, height=40):
        self._board_matrix = self.make_initial_board(width, height)

    def make_initial_board(self, width, height):
        return [[None for _ in range(width)] for _ in range(height)]

    def print_board(self):
        print(*self._board_matrix, sep='\n')

    def add_piece(self, row, column, piece):
        self._board_matrix[column][row] = piece


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
