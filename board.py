import random as r


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
        return any(bracket_moves)

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

    def draw_board(self, player):
        draw = '    %s\n' % '   '.join(map(str, range(self.SIZE)))
        for row in range(self.SIZE):
            draw += '  +%s\n%d ' % (''.join(self.SIZE*(3*'-'+'+')), row)
            for col in range(self.SIZE):
                if self.is_legal((row, col), player):
                    draw += '| . '
                else:
                    draw += '| %s ' % self.board[row][col]
            draw += '|\n'
        draw += '  +%s' % ''.join(self.SIZE*(3*'-'+'+'))
        print(draw)
        print("Score O:%s @:%s" % self.score())

# SIZE = 8
# WHITE, BLACK, EMPTY = 'O', '@', ' '
# DIRECTIONS = {  # row, col coordinates
#     'UP': (-1, 0), 'DOWN': (1, 0),
#     'RIGHT': (0, 1), 'LEFT': (0, -1),
#     'UP_RIGHT': (-1, 1), 'UP_LEFT': (-1, -1),
#     'DOWN_RIGHT': (1, 1), 'DOWN_LEFT': (1, -1)
# }
#
# SQUARE_WEIGHT = [
#     120, -20, 20,  5,  5, 20, -20, 120,
#     -20, -40, -5, -5, -5, -5, -40, -20,
#     20,   -5, 15,  3,  3, 15,  -5,  20,
#     5,    -5,  3,  3,  3,  3,  -5,   5,
#     5,    -5,  3,  3,  3,  3,  -5,   5,
#     20,   -5, 15,  3,  3, 15,  -5,  20,
#     -20, -40, -5, -5, -5, -5, -40, -20,
#     120, -20, 20,  5,  5, 20, -20, 120,
# ]
#
#
# def opponent(player):
#     return BLACK if player is WHITE else WHITE
#
#
# def new_board():
#     assert SIZE % 2 == 0
#     board = [[EMPTY]*SIZE for x in range(SIZE)]
#     mid = (SIZE-2)//2
#     board[mid][mid] = WHITE
#     board[mid][SIZE-1-mid] = BLACK
#     board[SIZE-1-mid][mid] = BLACK
#     board[SIZE-1-mid][SIZE-1-mid] = WHITE
#     return board
#
#
# def in_bounds(row, col):
#     return (0 <= row < SIZE) and (0 <= col < SIZE)
#
#
# def find_bracket(move, direction, player, board):
#     """Search in one direction if there is a bracket"""
#     row, col = move
#     dy, dx = direction  # direction displacement
#     row += dy
#     col += dx
#     if not in_bounds(row, col) or board[row][col] == player:
#         return None
#     opp = opponent(player)
#     while board[row][col] == opp:  # Opponent disks in straight line until bracket
#         row += dy
#         col += dx
#         if not in_bounds(row, col):  # Entire board was search in the given direction, no bracket found
#             return None
#     return (row, col) if board[row][col] is player else None
#
#
# def is_legal(move, player, board):
#     """Search in all directions if a capture is made"""
#     row, col = move
#     if not in_bounds(row, col) or board[row][col] != EMPTY:
#         return False
#     bracket_moves = []  # Boolean list if there was a capture in a direction
#     for direction in DIRECTIONS.values():
#         bracket_moves.append(find_bracket(move, direction, player, board))
#     return board[row][col] == EMPTY and any(bracket_moves)
#
#
# def legal_moves(player, board):
#     moves = []
#     for row in range(SIZE):
#         for col in range(SIZE):
#             move = row, col
#             if is_legal(move,player,board):
#                 moves.append(move)
#     return moves if moves else None
#
#
# def make_move(move, player, board):
#     row, col = move
#     board[row][col] = player
#     for direction in DIRECTIONS.values():
#         make_flips(move, direction, player, board)
#     return board
#
#
# def make_flips(move, direction, player, board):
#     bracket = find_bracket(move, direction, player, board)
#     if bracket:
#         row, col = move
#         dy, dx = direction
#         row += dy
#         col += dx
#         while row != bracket[0] or col != bracket[1]:
#             board[row][col] = player
#             row += dy
#             col += dx
#
#
# def rand_move(player, board):
#     """Selects a random move for player"""
#     valid_moves = legal_moves(player, board)
#     return r.choice(valid_moves) if valid_moves else None
#
#
# def score(board):
#     W = B = 0
#     for row in range(SIZE):
#         for col in range(SIZE):
#             if board[row][col] == BLACK:
#                 B += 1
#             elif board[row][col] == WHITE:
#                 W += 1
#     return W, B
#
#
# def evaluation(player, board):
#     def mobility():
#         mine = legal_moves(player, board)
#         opp = opponent(player)
#         his = legal_moves(opp, board)
#         return len(mine) - len(his)
#
#     def coin_parity():
#         if player == WHITE:
#             mine, his = score(board)
#         else:
#             his, mine = score(board)
#         return mine - his
#
#     def corners():
#         opp = opponent(player)
#         total = 0
#         for row in range(SIZE):
#             for col in range(SIZE):
#                 if board[row][col] == player:
#                     total += SQUARE_WEIGHT[row][col]
#                 elif board[row][col] == opp:
#                     total -= SQUARE_WEIGHT[row][col]
#         return total
#     pass
#
#
# def draw_board(player, board):
#     draw = '    %s\n' % '   '.join(map(str, range(SIZE)))
#     for row in range(SIZE):
#         draw += '  +%s\n%d ' % (''.join(SIZE*(3*'-'+'+')), row)
#         for col in range(SIZE):
#             if is_legal((row, col), player, board):
#                 draw += '| . '
#             else:
#                 draw += '| %s ' % board[row][col]
#         draw += '|\n'
#     draw += '  +%s' % ''.join(SIZE*(3*'-'+'+'))
#     print(draw)
#     print("Score O:%s @:%s" % score(board))


# if __name__ == '__main__':
#     board = new_board()
#     player = BLACK
#     draw_board(player, board)
#     while True:
#         move = [int(x) for x in input("(%s) row col > " % player).split()]
#         if is_legal(move, player, board):
#             make_move(move, player, board)
#             player = opponent(player)
#             draw_board(player, board)
#             move = rand_move(player, board)
#             make_move(move, player, board)
#             player = opponent(player)
#             draw_board(player, board)
#             print("Player %s moved" % player, move)
#         else:
#             print("Try a valid move:", legal_moves(player, board))
