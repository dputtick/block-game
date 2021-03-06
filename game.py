import random


N_PIECES = 100
AGING_TIME = 1000
WIDTH = 20
PROBS = {
    'red': 0.2,
    'yellow': 0.3,
    'green': 0.4,
    'gray': 0.1
}
BREAK_PROBS = {
    'red': 0.3,
    'yellow': 0.2,
    'green': 0.1,
    'gray': 0
}
GRAY_CHANGE_PROB = 0.2


class Game():

    def __init__(self):
        self.board = Board()
        self.piece_queue = [Piece.random_piece_factory() for _ in range(N_PIECES)]

    def play(self):
        """Run the main game loop."""
        while self.piece_queue:
            self._normal_turn()
        for _ in range(AGING_TIME):
            self.board.check_breakage()
            self.board.show()

    def _normal_turn(self):
        """Run one round of the normal, pre-aging move process."""
        new_piece = self.piece_queue.pop()
        column, row = self._get_player_move(new_piece)
        self.board.add_piece(column, row, new_piece)
        self.board.check_breakage()
        self.board.break_pieces()

    def _get_player_move(self, piece):
        """Get the player's choice of column and row for their next move."""
        self.board.show()
        print("Current piece: {}".format(piece.color))
        if self.piece_queue:
            print("Next piece: {}".format(self.piece_queue[-1].color))
        valid_moves = self.board.get_valid_moves()
        input_str = input("Enter the column and row to place your piece in:\n")
        column, row = (int(n) for n in input_str.split(' '))
        while (column, row) not in valid_moves:
            column, row = (int(n) for n in input("Please enter a valid move:\n").split(' '))
        return column, row


class Board():

    def __init__(self, width=5, height=40):
        self._board_matrix = self._make_initial_board(width, height)

    def _make_initial_board(self, width, height):
        """Setup the internal representation of the board."""
        board = []
        for n in range(height):
            if n % 2 == 0:
                board.append([None for _ in range(width)])
            else:
                board.append([None for _ in range(width - 1)])
        return board

    def show(self):
        """Print a representation of the current board state."""
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

    def check_pieces(self):
        """Check all placed pieces for breakage/color change."""
        for row, row_list in enumerate(self._board_matrix):
            for col, location in enumerate(row_list):
                if isinstance(location, Piece):
                    if location.color == 'gray':
                        location.check_gray_change()
                    else:
                        location.will_break = location.check_should_break()
                        if not location.will_break and row != 0:
                            lchild, rchild = self.get_pieces_below(col, row)
                            if lchild is None or lchild.will_break:
                                if rchild is None or rchild.will_break:
                                    location.will_break = True

    def break_pieces(self):
        """Change all pieces with `will_break` attribute to `None`."""
        for row, row_list in enumerate(self._board_matrix):
            for col, location in enumerate(row_list):
                if isinstance(location, Piece) and location.will_break:
                    self._board_matrix[row][col] = None


class Piece():

    def __init__(self, color):
        self.color = color
        self.break_probability = BREAK_PROBS[color]
        self.will_break = False

    def __repr__(self):
        return '<Piece: {}>'.format(str(self.color))

    def __str__(self):
        return self.color

    @staticmethod
    def random_piece_factory():
        """Return a Piece randomly chosen using the configured weights."""
        colors, weights = zip(*PROBS.items())
        (color,) = random.choices(colors, weights=weights)
        return Piece(color)

    def check_should_break(self):
        """Use the breakage probability to decide whether the piece breaks."""
        return random.random() < self.break_probability

    def check_gray_change(self):
        """Check whether a gray piece should change into another color."""
        if self.color == 'gray':
            if random.random() < GRAY_CHANGE_PROB:
                colors, weights = zip(*PROBS.items())
                (color,) = random.choices(colors, weights=weights)
                self.color = color
                self.break_probability = BREAK_PROBS[color]


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
