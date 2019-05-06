import random
from copy import deepcopy


class Agent:
    # SQUARE_WEIGHT = [
    #     [120, -20, 20,  5,  5, 20, -20, 120],
    #     [-20, -40, -5, -5, -5, -5, -40, -20],
    #     [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    #     [  5,  -5,  3,  3,  3,  3,  -5,   5],
    #     [  5,  -5,  3,  3,  3,  3,  -5,   5],
    #     [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    #     [-20, -40, -5, -5, -5, -5, -40, -20],
    #     [120, -20, 20,  5,  5, 20, -20, 120]
    # ]
    SQUARE_WEIGHT = [
        [120, -20, 20,  15,  15, 20, -20, 120],
        [-20, -40, -5,  -5,  -5, -5, -40, -20],
        [ 20,  -5, 10,   3,   3, 10,  -5,  20],
        [ 15,  -5,  3,   3,   3,  3,  -5,  15],
        [ 15,  -5,  3,   3,   3,  3,  -5,  15],
        [ 20,  -5, 10,   3,   3, 10,  -5,  20],
        [-20, -40, -5,  -5,  -5, -5, -40, -20],
        [120, -20, 20,  15,  15, 20, -20, 120]
    ]

    MAX = 10000
    MIN = -MAX

    def __init__(self, color, level, depth):
        self.color = color
        self.level = level
        self.depth = depth

    def evaluate(self, player, board):
        opp = board.opponent(player)
        corners = 0
        discs = 0
        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.board[row][col] == player:
                    discs += 1
                    corners += self.SQUARE_WEIGHT[row][col]
                elif board.board[row][col] == opp:
                    discs -= self.SQUARE_WEIGHT[row][col]
                    corners -= self.SQUARE_WEIGHT[row][col]

        def mobility():
            mine = board.legal_moves(player)
            opponent = board.opponent(player)
            theirs = board.legal_moves(opponent)
            return len(mine) - len(theirs)

        if board.end_of_game():
            if discs < 0:
                return self.MIN
            elif discs > 0:
                return self.MAX
            else:
                return discs

        if self.level == 0:
            return random.randint(-30, 30)
        elif self.level == 1:
            return discs
        elif self.level == 2:
            return mobility()
        elif self.level == 3:
            return corners
        elif self. level == 4:
            if board.num_discs < 34:
                return mobility()+corners
            else:
                return discs

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
            new_value = -self.negamax(board.opponent(player), try_move(m), depth-1)[0]
            if new_value >= value:
                value = new_value
                best_move = m
        return value, best_move

    def negamax_AB(self, player, board, depth, alpha, beta):
        if depth == 0 or board.end_of_game():
            return self.evaluate(player, board), None

        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        moves = board.legal_moves(player)

        if not moves:  # Current player has no move
            return self.evaluate(player, board), None

        best_move = moves[0]
        for m in moves:
            if alpha >= beta:
                break
            value = -self.negamax_AB(board.opponent(player), try_move(m), depth-1, -beta, -alpha)[0]
            if value > alpha:
                alpha = value
                best_move = m
        return alpha, best_move

    def best_move(self, board):
        return self.negamax_AB(self.color, board, self.depth, self.MIN, self.MAX)[1]
