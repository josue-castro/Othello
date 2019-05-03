

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
        self.board = self.new_board()

    def new_board(self):
        board = [[self.EMPTY] * self.SIZE for x in range(self.SIZE)]
        mid = (self.SIZE - 2) // 2
        board[mid][mid] = self.WHITE
        board[mid][self.SIZE - 1 - mid] = self.BLACK
        board[self.SIZE - 1 - mid][mid] = self.BLACK
        board[self.SIZE - 1 - mid][self.SIZE - 1 - mid] = self.WHITE
        return board

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
        bracket_moves = []  # Boolean list if there was a capture in a direction
        for direction in self.DIRECTIONS.values():
            bracket_moves.append(self.find_bracket(move, direction, player))
        return self.board[row][col] == self.EMPTY and any(bracket_moves)

    def legal_moves(self, player):
        moves = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                move = row, col
                if self.is_legal(move, player):
                    moves.append(move)
        return moves if moves else None

    def make_move(self, move, player):
        row, col = move
        self.board[row][col] = player
        for direction in self.DIRECTIONS.values():
            self.make_flips(move, direction, player)

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
        W = B = 0
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.board[row][col] == self.BLACK:
                    B += 1
                elif self.board[row][col] == self.WHITE:
                    W += 1
        return W, B

    def next_turn(self, player):
        opp = self.opponent(player)
        if self.legal_moves(opp):
            return opp
        elif self.legal_moves(player):  # opponent passed
            print("Player %s passed" % opp)
            return player
        else:
            return None

    def end_of_game(self):
        return not self.legal_moves(self.WHITE) and not self.legal_moves(self.BLACK)

    def draw_board(self, player):
        draw = ''
        draw += '    %s\n' % '   '.join(map(str, range(self.SIZE)))
        for row in range(self.SIZE):
            draw += '  +%s\n%d ' % (''.join(self.SIZE*(3*'-'+'+')), row)
            for col in range(self.SIZE):
                if self.is_legal((row, col), player):
                    draw += '| . '
                else:
                    draw += '| %s ' % self.board[row][col]
            draw += '|\n'
        draw += '  +%s\n' % ''.join(self.SIZE*(3*'-'+'+'))
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # draw += '    %s\n' % '   '.join(abc)
        print(draw + "\nScore O:%s @:%s" % self.score())

    def draw_abc(self, player):
        draw = ''
        for row in range(self.SIZE):
            draw += '  +%s\n%d ' % (''.join(self.SIZE*(3*'-'+'+')), self.SIZE - row)
            for col in range(self.SIZE):
                if self.is_legal((row, col), player):
                    draw += '| . '
                else:
                    draw += '| %s ' % self.board[row][col]
            draw += '|\n'
        draw += '  +%s\n' % ''.join(self.SIZE*(3*'-'+'+'))
        draw += '    %s\n' % '   '.join(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        print(draw + "\nScore O:%s @:%s" % self.score())

