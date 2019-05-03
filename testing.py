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
        print("Score O:%d @:%d" % board.score(board.WHITE))
        print("Player %s" % player)
        if player == rand_agent.player:
            move = rand_agent.negamax(player, board, 2)[1]
            board.make_move(move, player)
        else:
            move = ai_agent.negamax(player, board, 2)[1]
            board.make_move(move, player)
        if board.end_of_game():
            board.draw_board(player)
            print("Game Over! O:%d @:%d" % board.score(board.WHITE))
            sys.exit(0)
        # os.system('clear')

