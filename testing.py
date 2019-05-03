import os, sys
from agent import Agent
from board import Board

if __name__ == '__main__':
    board = Board()
    rand_agent = Agent(board.WHITE, 2)
    ai_agent = Agent(board.opponent(rand_agent.player), 3)
    player = board.WHITE
    while True:
        player = board.next_turn(player)
        board.draw_board(player)
        print("Player %s" % player)
        if player == rand_agent.player:
            move = rand_agent.negamax(player, board, 2)[1]
            board.make_move(move, player)
        elif player == ai_agent.player:
            move = ai_agent.negamax(player, board, 2)[1]
            board.make_move(move, player)
        else:
            print("Game Over! O:%s @:%s" % board.score())
            sys.exit(0)
        os.system('clear')

