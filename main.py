from board import Board
from agent import Agent
from copy import deepcopy
if __name__ == '__main__':
    board = Board()
    agent = Agent(board.WHITE, 3)
    player = board.BLACK
    board.draw_board(player)
    while True:
        move = [int(x) for x in input("(%s) row col > " % player).split()]
        if board.is_legal(move, player):
            board.make_move(move, player)
            player = board.opponent(player)
            board.draw_board(player)
            if player == board.WHITE:
                print(agent.negamax(player, board, 1))
        else:
            print("Try a valid move:", board.legal_moves(player))

