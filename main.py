import os, sys
from board import Board
from agent import Agent
from time import sleep

# def get_move(move):
#     abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#     if (move.index() not in abc) or (move.index() not in map(str, range(1, 9))):
#         return None
#     row = 8-int(move[1])
#     col = abc.index(move[0])
#     return row, col

if __name__ == '__main__':
    board = Board()
    user = board.BLACK
    agent = Agent(board.opponent(user), 1)
    player = board.WHITE
    while True:
        player = board.next_turn(player)
        board.draw_board(player)
        print("Score O:%d @:%d" % board.score(board.WHITE))
        if player == user:
            while True:
                move = input("(%s) row col > " % player).split()
                move = tuple(map(int, move))
                if board.is_legal(move, player):
                    board.make_move(move, player)
                    break
                else:
                    print("Try a valid move:", board.legal_moves(player))
        else:
            move = agent.negamax(player, board, 3)[1]
            board.make_move(move, player)
            print("Player %s moved" % player, move)
        if board.end_of_game():
            board.draw_board(player)
            print("Game Over! O:%d @:%d" % board.score(board.WHITE))
            sys.exit(0)
        os.system('clear')
