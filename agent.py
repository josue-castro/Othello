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
    MAX = 10000
    MIN = -MAX

    def __init__(self, player, level):
        self.player = player
        self.level = level

    def rand_move(self, board):
        return choice(board.legal_moves(self.player))

    def evaluate(self, player, board):
        def coin_parity():
            mine, theirs = board.score(player)
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

        if board.end_of_game():
            diff = coin_parity()
            if diff < 0:
                return self.MIN
            elif diff > 0:
                return self.MAX
            else:
                return diff
        elif self.level == 1:
            return coin_parity()
        elif self.level == 2:
            return mobility()
        elif self.level == 3:
            return corners()

    def negamax(self, player, board, depth):
        if depth == 0 or board.end_of_game():
            return self.evaluate(player, board), None

        value = self.MIN

        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        moves = board.legal_moves(player)

        if not moves:  # Current player has no move
            return self.evaluate(player, board), None

        best_move = moves[0]
        for m in moves:
            value, best_move = max((value, best_move), (-self.negamax(board.opponent(player), try_move(m), depth-1)[0], m))
        return value, best_move

    def negamax_AB(self, player, board, depth, alpha, beta):
        if depth == 0 or board.end_of_game():
            return self.evaluate(player, board), None
        value = self.MIN

        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        moves = board.legal_moves(player)

        if not moves:  # Current player has no move
            return self.evaluate(player, board), None

        best_move = moves[0]
        for m in moves:
            value, best_move = max((value, best_move), (-self.negamax_AB(board.opponent(player), try_move(m), depth-1, -beta, -alpha)[0], m))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
