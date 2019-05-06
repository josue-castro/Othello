import os, sys
from time import time
from agent import Agent
from board import Board

if __name__ == '__main__':
    board = Board()
    players = {
        Board.BLACK: (Agent(Board.BLACK, 5, 5), []),
        Board.WHITE: (Agent(Board.WHITE, 4, 5), [])
    }

    turn = Board.BLACK
    board.draw_board(turn)
    while not board.end_of_game():
        agent = players[turn][0]
        start = time()
        move = agent.best_move(board)
        # move = agent.negamax(agent.color, board, agent.depth,)[1]
        end = time()
        players[turn][1].append(end-start)
        board.make_move(move, turn)
        prev_turn = turn
        turn = board.next_turn(turn)
        board.draw_board(turn)
        print(prev_turn+"'s move", move)
        print("Your turn %s" % turn)
    for player in players:
        print("Player %s avg = %dms, max = %dms" % (player, sum(players[player][1]) * 1000 / len(players[player][1]), max(players[player][1]) * 1000))

