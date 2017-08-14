import random

from enum import Enum


N_PIECES = 100
AGING = 1000
WIDTH = 20
P_RED = 0.1
P_YELLOW = 0.05
P_GREEN = 0.001


class Game():

    def __init__(self):
        self.board = Board()
        self.piece_queue = [self._random_piece() for _ in range(N_PIECES)]

    def play(self):
        while self.piece_queue:
            self._normal_turn()
        for _ in range(AGING):
            self._check_breakage()
            self.board.show()
            # randomly cause avalanches

    def _normal_turn(self):
        new_piece = self.piece_queue.pop()
        column = self._get_player_move(new_piece)
        self.board.add_piece(column, new_piece)
        self._check_breakage()

    def _random_piece(self):
        piece_type = random.choice(list(PieceType.__members__.values()))
        return Piece(piece_type)

    def _get_player_move(self, piece):
        self.board.show()
        column = int(input("Enter the column you'd like to place your piece in:\n"))
        while not self.board.check_valid_move(column):
            column = int(input("That column is full. Enter a valid move:\n"))
        return column

    def _check_breakage(self):
        pass


class Board():

    def __init__(self, width=5, height=40):
        self._board_matrix = self.make_initial_board(width, height)

    def make_initial_board(self, width, height):
        return [[None for _ in range(width)] for _ in range(height)]

    def show(self):
        print(*reversed(self._board_matrix), sep='\n')

    def add_piece(self, column, piece):
        for row_n, row in enumerate(self._board_matrix):
            if row[column] is None:
                self._board_matrix[row_n][column] = piece
                return

    def check_valid_move(self, column):
        return True


class PieceType(Enum):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'
    # GRAY = 'gray'


class Piece():

    def __init__(self, input_type):
        self.type = PieceType(input_type)

    def __repr__(self):
        return '<Piece: type {}>'.format(str(self.type))


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
