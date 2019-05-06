from colorama import Fore


class Board:
    SIZE = 8
    WHITE, BLACK = 'O', '@'
    EMPTY = ' '
    DIRECTIONS = {  # row, col coordinates
        'UP': (-1, 0), 'DOWN': (1, 0),
        'RIGHT': (0, 1), 'LEFT': (0, -1),
        'UP_RIGHT': (-1, 1), 'UP_LEFT': (-1, -1),
        'DOWN_RIGHT': (1, 1), 'DOWN_LEFT': (1, -1)
    }

    def __init__(self):
        self.board, self.empty_squares = self.new_board()
        self.num_discs = 4

    def new_board(self):
        board = [[self.EMPTY] * self.SIZE for x in range(self.SIZE)]
        board[3][3] = self.WHITE
        board[3][4] = self.BLACK
        board[4][3] = self.BLACK
        board[4][4] = self.WHITE

        empty_squares = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                empty_squares.append((row, col))

        empty_squares.remove((3, 3))
        empty_squares.remove((3, 4))
        empty_squares.remove((4, 3))
        empty_squares.remove((4, 4))
        return board, empty_squares

    def in_bounds(self, row, col):
        return (0 <= row < self.SIZE) and (0 <= col < self.SIZE)

    def opponent(self, player):
        return self.BLACK if player is self.WHITE else self.WHITE

    def find_bracket(self, move, direction, player):
        """Search in one direction if there is a bracket"""
        row, col = move
        dy, dx = direction  # direction displacement
        row += dy
        col += dx
        if not self.in_bounds(row, col) or self.board[row][col] == player:
            return None
        opp = self.opponent(player)
        while self.board[row][col] == opp:  # Opponent disks in straight line until bracket
            row += dy
            col += dx
            if not self.in_bounds(row, col):  # Entire board was search in the given direction, no bracket found
                return None
        return (row, col) if self.board[row][col] is player else None

    def is_legal(self, move, player):
        """Search in all directions if a capture is made"""
        row, col = move
        if not self.in_bounds(row, col) or self.board[row][col] != self.EMPTY:
            return False
        for direction in self.DIRECTIONS.values():
            if self.find_bracket(move, direction, player):
                return True
        return False

    def legal_moves(self, player):
        moves = []
        for move in self.empty_squares:
            if self.is_legal(move, player):
                moves.append(move)
        return moves  # A lo mejor tengo que retornar None

    def make_move(self, move, player):
        row, col = move
        self.board[row][col] = player
        for direction in self.DIRECTIONS.values():
            self.make_flips(move, direction, player)
        self.num_discs += 1
        self.empty_squares.remove(move)

    def make_flips(self, move, direction, player):
        bracket = self.find_bracket(move, direction, player)
        if bracket:
            row, col = move
            dy, dx = direction
            row += dy
            col += dx
            while row != bracket[0] or col != bracket[1]:
                self.board[row][col] = player
                row += dy
                col += dx

    def score(self):
        w = b = 0
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.board[row][col] == self.WHITE:
                    w += 1
                elif self.board[row][col] == self.BLACK:
                    b += 1
        return w, b

    def next_turn(self, player):
        opp = self.opponent(player)
        if self.has_move(opp):
            return opp
        elif self.has_move(player):  # opponent passed
            print("\nPlayer %s passed ...\n" % opp)
            return player
        else:
            return None

    def end_of_game(self):
        return not self.has_move(self.WHITE) and not self.has_move(self.BLACK)

    def has_move(self, player):
        for move in self.empty_squares:
            if self.is_legal(move, player):
                return True

    def draw_board(self, player):
        draw = ''
        draw += '    %s ' % '   '.join(map(str, range(self.SIZE)))
        draw += "  Score O:%d @:%d\n" % self.score()
        for row in range(self.SIZE):
            draw += '  +%s\n%d ' % (''.join(self.SIZE*(3*'-'+'+')), row)
            for col in range(self.SIZE):
                if self.is_legal((row, col), player):
                    draw += '| . '
                else:
                    draw += '| %s ' % self.board[row][col]
            draw += '|\n'
        draw += '  +%s\n' % ''.join(self.SIZE*(3*'-'+'+'))
        print(draw)

    def draw_color_board(self, player):
        draw = ''
        draw += '    %s ' % '   '.join(map(str, range(self.SIZE)))
        draw += "  Score O:%d @:%d\n" % self.score()
        for row in range(self.SIZE):
            draw += '  +%s\n%d ' % (''.join(self.SIZE * (3 * '-' + '+')), row)
            for col in range(self.SIZE):
                if self.is_legal((row, col), player):
                    draw += '| . '  # + Fore.YELLOW + '. ' + Fore.BLACK
                elif self.board[row][col] == self.WHITE:
                    draw += '| ' + Fore.WHITE + 'O ' + Fore.BLACK
                else:
                    draw += '| %s ' % self.board[row][col]
            draw += '|\n'
        draw += '  +%s\n' % ''.join(self.SIZE * (3 * '-' + '+'))
        print(draw)
