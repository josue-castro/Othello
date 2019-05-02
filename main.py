from board import Board
from agent import Agent
from os import system


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
        if player == user:
            while True:
                move = input("(%s) row col > " % player).split()
                move = tuple(map(int, move))
                if board.is_legal(move, player):
                    board.make_move(move, player)
                    break
                else:
                    print("Try a valid move:", board.legal_moves(player))
        elif player == agent.player:
            move = agent.negamax(player, board, 3)[1]
            board.make_move(move, player)
        else:
            print("Game Over! O:%s @:%s" % board.score())
        system('clear')
