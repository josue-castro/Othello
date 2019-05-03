import os, sys
from time import time
from agent import Agent
from board import Board

if __name__ == '__main__':
    board = Board()
    rand_agent = Agent(board.WHITE, 2)
    ai_agent = Agent(board.opponent(rand_agent.player), 3)
    player = board.WHITE
    time_ply1 = []
    time_ply2 = []
    while not board.end_of_game():
        player = board.next_turn(player)
        board.draw_board(player)
        print("Score O:%d @:%d" % board.score(board.WHITE))
        print("Player %s" % player)
        if player == rand_agent.player:
            start = time()
            move = rand_agent.negamax_AB(player, board, 5, rand_agent.MIN, rand_agent.MAX)[1]
            end = time()
            time_ply1.append(end-start)
            board.make_move(move, player)
        else:
            start = time()
            move = ai_agent.negamax_AB(player, board, 5, ai_agent.MIN, ai_agent.MAX)[1]
            end = time()
            time_ply2.append(end-start)
            board.make_move(move, player)
        # os.system('clear')
    board.draw_board(player)
    print("Game Over! O:%d @:%d" % board.score(board.WHITE))
    print("Player 1 avgt = %dms, max = %dms" % ((sum(time_ply1)*1000/len(time_ply1)), max(time_ply1)*1000))
    print(time_ply1)
    print("Player 2 avgt = %dms, max = %dms" % ((sum(time_ply2)*1000/len(time_ply2)), max(time_ply2)*1000))
    print(time_ply2)
    sys.exit(0)


