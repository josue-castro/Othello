from random import choice
from copy import deepcopy


class Agent:
    SQUARE_WEIGHT = [
        [120, -20, 20,  5,  5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [ 20,  -5, 15,  3,  3, 15,  -5,  20],
        [  5,  -5,  3,  3,  3,  3,  -5,   5],
        [  5,  -5,  3,  3,  3,  3,  -5,   5],
        [ 20,  -5, 15,  3,  3, 15,  -5,  20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20,  5,  5, 20, -20, 120]
    ]

    def __init__(self, player, level):
        self.player = player
        self.level = level

    def rand_move(self, board):
        return choice(board.legal_moves(self.player))

    def evaluate(self, player, board):
        def coin_parity():
            if player == board.WHITE:
                mine, theirs = board.score()
            else:
                theirs, mine = board.score()
            return mine - theirs

        def mobility():
            mine = board.legal_moves(player)
            opp = board.opponent(player)
            theirs = board.legal_moves(opp)
            return len(mine) - len(theirs)

        def corners():
            opp = board.opponent(player)
            total = 0
            for row in range(board.SIZE):
                for col in range(board.SIZE):
                    if board.board[row][col] == player:
                        total += self.SQUARE_WEIGHT[row][col]
                    elif board.board[row][col] == opp:
                        total -= self.SQUARE_WEIGHT[row][col]
            return total

        if self.level == 1:
            return coin_parity()
        elif self.level == 2:
            return mobility()
        elif self.level == 3:
            return corners()

    def negamax(self, player, board, depth):
        if depth == 0:
            return self.evaluate(player, board), None
        value = -10000

        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        moves = board.legal_moves(player)
        best_move = None
        for m in moves:
            new_val = -self.negamax(board.opponent(player), try_move(m), depth - 1)[0]
            print(new_val, m)
            if new_val > value:
                value = new_val
                best_move = m
        return value, best_move




