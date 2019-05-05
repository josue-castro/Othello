import os, sys, time
from cfonts import say
from colorama import Fore, Back, init
from board import Board
from agent import Agent


if __name__ == '__main__':
    print(Back.CYAN)
    os.system('clear')
    say("Othello", font='block', align='center', colors=['white', 'black'])
    print(Fore.BLACK)
    print("1. Player vs Player\n2. Player vs AI\n3. AI vs Player\n4. AI vs AI")
    menu = int(input("Select: "))
    os.system('clear')
    level = depth = 3
    players = {}

    if menu == 1:
        pass
    elif menu == 2:
        players['O'] = Agent(Board.WHITE, level, depth)
    elif menu == 3:
        players['@'] = Agent(Board.WHITE, level, depth)
    elif menu == 4:
        players['@'] = Agent(Board.WHITE, 2, depth)
        players['O'] = Agent(Board.WHITE, level, depth)

    board = Board()
    turn = board.BLACK
    board.draw_board(turn)
    while not board.end_of_game():
        if turn in players:
            agent = players[turn]
            print(turn+" agent's turn")
            time.sleep(1)
            move = agent.negamax_AB(turn, board, 3, agent.MIN, agent.MAX)[1]
            board.make_move(move, turn)
        else:
            while True:
                move = input(turn+"'s turn (row col) > ").split()
                move = tuple(map(int, move))
                if board.is_legal(move, turn):
                    board.make_move(move, turn)
                    break
                else:
                    print("Try a valid move:", board.legal_moves(turn))
        os.system('clear')
        prev_turn = turn
        turn = board.next_turn(turn)
        board.draw_board(turn)
        print(prev_turn+"'s move", move)
    print("Game Over!\n")
    sys.exit(0)
