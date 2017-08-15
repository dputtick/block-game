import random


N_PIECES = 100
AGING_TIME = 1000
WIDTH = 20
PROBS = {
    'red': 0.2,
    'yellow': 0.4,
    'green': 0.4
}
BREAK_PROBS = {
    'red': 0.5,
    'yellow': 0.2,
    'green': 0.1
}


class Game():

    def __init__(self):
        self.board = Board()
        self.piece_queue = [Piece.random_piece_factory() for _ in range(N_PIECES)]

    def play(self):
        while self.piece_queue:
            self._normal_turn()
        for _ in range(AGING_TIME):
            self.board.check_breakage()
            self.board.show()

    def _normal_turn(self):
        new_piece = self.piece_queue.pop()
        column, row = self._get_player_move(new_piece)
        self.board.add_piece(column, row, new_piece)
        self.board.check_breakage()
        self.board.break_pieces()

    def _get_player_move(self, piece):
        self.board.show()
        print("Current piece: {}".format(piece.type))
        if self.piece_queue:
            print("Next piece: {}".format(self.piece_queue[-1].type))
        valid_moves = self.board.get_valid_moves()
        instring = input("Enter the column and row you'd like to place your piece in:\n")
        column, row = (int(n) for n in instring.split(' '))
        while (column, row) not in valid_moves:
            column, row = (int(n) for n in input("Please enter a valid move:\n").split(' '))
        return column, row


class Board():

    def __init__(self, width=5, height=40):
        self._board_matrix = self.make_initial_board(width, height)

    def make_initial_board(self, width, height):
        board = []
        for n in range(height):
            if n % 2 == 0:
                board.append([None for _ in range(width)])
            else:
                board.append([None for _ in range(width - 1)])
        return board

    def show(self):
        print(*reversed(self._board_matrix), sep='\n')

    def add_piece(self, column, row, piece):
        """Add a piece to the board at a given location."""
        self._board_matrix[row][column] = piece

    def get_pieces_below(self, column, row):
        """Take a location on the board and returns the values of the two pieces below it."""
        try:
            if row % 2 == 0:
                l_child = self._board_matrix[row - 1][column - 1]
            else:
                l_child = self._board_matrix[row - 1][column]
        except IndexError:
            l_child = None
        try:
            if row % 2 == 0:
                r_child = self._board_matrix[row - 1][column]
            else:
                r_child = self._board_matrix[row - 1][column + 1]
        except IndexError:
            r_child = None
        return l_child, r_child

    def get_valid_moves(self):
        """Return a list of valid move locations as tuples (column, row)."""
        valid_moves = []
        for row, row_list in enumerate(self._board_matrix):
            for col, location in enumerate(row_list):
                if location is None:
                    if row == 0:
                        valid_moves.append((col, row))
                    elif self.get_pieces_below(col, row) != (None, None):
                        valid_moves.append((col, row))
        return valid_moves

    def check_breakage(self):
        """Iterate through all placed pieces and check if they should break."""
        for row, row_list in enumerate(self._board_matrix):
            for col, location in enumerate(row_list):
                if location is not None:
                    location.will_break = location.should_break()
                    if location.will_break is False and row != 0:
                        lchild, rchild = self.get_pieces_below(col, row)
                        if lchild is None or lchild.will_break:
                            if rchild is None or rchild.will_break:
                                location.will_break = True

    def break_pieces(self):
        for row, row_list in enumerate(self._board_matrix):
            for col, location in enumerate(row_list):
                if location and location.will_break:
                    self._board_matrix[row][col] = None


class Piece():

    def __init__(self, input_type):
        print(input_type)
        self.type = input_type
        self.break_probability = BREAK_PROBS[input_type]
        self.will_break = False

    def __repr__(self):
        return '<Piece: type {}>'.format(str(self.type))

    def __str__(self):
        return self.type

    @staticmethod
    def random_piece_factory():
        """Return a Piece randomly chosen using the configured weights."""
        colors, weights = zip(*PROBS.items())
        (color,) = random.choices(colors, weights=weights)
        return Piece(color)

    def should_break(self):
        """Use the breakage probability to decide whether the piece breaks."""
        return random.random() < self.break_probability


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
