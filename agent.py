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
        [100, -20, 20,  20,  20, 20, -20, 100],
        [-20, -40, -1,  -1,  -1, -1, -40, -20],
        [ 20,  -1,  3,   1,   1,  3,  -1,  20],
        [ 20,  -1,  1,   2,   2,  1,  -1,  20],
        [ 20,  -1,  1,   2,   2,  1,  -1,  20],
        [ 20,  -1,  3,   1,   1,  3,  -1,  20],
        [-20, -40, -1,  -1,  -1, -1, -40, -20],
        [100, -20, 20,  20,  20, 20, -20, 100]
    ]

    MAX = 10000
    MIN = -MAX

    def __init__(self, color, level, depth):
        self.color = color
        self.level = level
        self.depth = depth

    def evaluate(self, player, board):
        """The evaluate method calculates balanced evaluators,
        this means the advantage for one player results in an
        equal but opposite disadvantage for the other player.
        Still we use them from the players perspective
        """
        # RANDOM MOVE
        if self.level == 0:
            return random.randint(-30, 30)

        # CALCULATE ALL POSSIBLE HEURISTIC TO SAVE TIME IN A SINGLE TRAVERSE
        opp = board.opponent(player)
        corners = 0
        discs = 0
        mobility = 0

        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.board[row][col] == player:
                    discs += 1
                    corners += self.SQUARE_WEIGHT[row][col]
                elif board.board[row][col] == opp:
                    discs -= 1
                    corners -= self.SQUARE_WEIGHT[row][col]

                # ONLY CALCULATE MOBILITY IF NECESSARY, IT TAKES MORE TIME
                if self.level == 1 or self.level == 5 or (self.level == 4 and len(board.empty_squares) <= 30):
                    if board.is_legal((row, col), player):
                        mobility += 1
                    if board.is_legal((row, col), opp):
                        mobility -= 1

        # END OF GAME
        # RETURN -INF OR +INF
        if board.end_of_game():
            return self.final_value(player, board)

        # RETURN THE EVALUATION ACCORDING TO LEVEL
        if self.level == 1:
            return mobility
        elif self.level == 2:
            return discs
        elif self.level == 3:
            return corners
        elif self.level == 4:
            if len(board.empty_squares) > 30:
                return corners
            else:
                return discs+mobility
        elif self.level == 5:
            return corners+discs+mobility

    def negamax(self, player, board, depth):
        if depth == 0:
            return self.evaluate(player, board), None

        value = self.MIN

        # DEEP COPY BOARD AFTER MAKING TO AVOID ALTERATION
        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        # CHILD NODES
        moves = board.legal_moves(player)
        # CURRENT PLAYER HAS NO MOVE
        if not moves:  # Current player has no move
            if not board.has_move(board.opponent(player)):
                return self.final_value(player, board), None  # GAME ENDED RETURN FINAL VALUE
            return self.evaluate(player, board), None  # PLAYER PASSED, RETURN EVALUATION

        best_move = moves[0]
        for m in moves:
            new_value = -self.negamax(board.opponent(player), try_move(m), depth-1)[0]
            if new_value >= value:
                value = new_value
                best_move = m
        return value, best_move

    def negamax_AB(self, player, board, depth, alpha, beta):
        if depth == 0:
            return self.evaluate(player, board), None

        # DEEP COPY BOARD AFTER MAKING TO AVOID ALTERATION
        def try_move(move):
            temp_board = deepcopy(board)
            temp_board.make_move(move, player)
            return temp_board

        # CHILD NODES
        moves = board.legal_moves(player)
        # CURRENT PLAYER HAS NO MOVE
        if not moves:
            if not board.has_move(board.opponent(player)):
                return self.final_value(player, board), None  # GAME ENDED RETURN FINAL VALUE
            return self.evaluate(player, board), None  # PLAYER PASSED, RETURN EVALUATION

        best_move = moves[0]
        for m in moves:
            if alpha >= beta:
                break  # PRUNE

            value = -self.negamax_AB(board.opponent(player), try_move(m), depth-1, -beta, -alpha)[0]
            if value > alpha:
                alpha = value
                best_move = m
        return alpha, best_move

    def best_move(self, board):
        """Simplified negamax alpha-beta call"""
        return self.negamax_AB(self.color, board, self.depth, self.MIN, self.MAX)[1]

    def final_value(self, player, board):
        """Calculate score when game has ended and return +/- inf evaluation"""
        score = 0
        opp = board.opponent(player)
        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.board[row][col] == player:
                    score += 1
                elif board.board[row][col] == opp:
                    score -= 1
        if score < 0:
            return self.MIN
        elif score > 0:
            return self.MAX
        else:
            return score
