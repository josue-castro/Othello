import os, sys, time
from cfonts import say
from colorama import Fore, Back, Style
from board import Board
from agent import Agent

DEFAULT_LEVEL = 1
DEFAULT_DEPTH = 2


def exit_app():
    print("Exit!")
    time.sleep(1)
    print(Style.RESET_ALL)
    os.system('clear')
    sys.exit(0)


def clean_line(n):
    time.sleep(1)
    for x in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def valid_play(user_input):
    if len(user_input.split()) != 2:
        return []
    for x in user_input.split():
        if not x.isnumeric():
            return []
    return [int(x) for x in user_input.split()]


def configure_agent(color):
    print("DEFAULT=1".rjust(40), flush=True, end='\r')
    level = input("%s's difficulty (1-3): " % color)
    while not level.isnumeric():
        print("Try a Valid Option!")
        clean_line(2)
        level = input("%s's difficulty (1-3): " % color)
    level = int(level) if 0 < int(level) <= 3 else DEFAULT_LEVEL
    print("DEFAULT=2".rjust(40), flush=True, end='\r')
    depth = input("%s's depth (1-6): " % color)
    while not depth.isnumeric():
        print("Try a Valid Option!")
        clean_line(2)
        depth = input("%s's depth (1-6): " % color)
    depth = int(depth) if 0 < int(depth) <= 6 else DEFAULT_DEPTH
    os.system('clear')
    return level, depth


if __name__ == '__main__':
    # Setting up menu and options
    while True:
        print(Back.CYAN)
        os.system('clear')
        say("Othello", font='block', align='center', colors=['white', 'black'])
        print(Fore.BLACK)
        print("1. Player vs Player\n2. Player vs AI\n3. AI vs Player\n4. AI vs AI\n")
        print("\t\tPress ENTER to Exit", flush=True, end='\r')
        menu = input("Select: ")
        while True:
            if not menu:
                exit_app()
            elif menu.isnumeric() and 0 < int(menu) <= 4:
                menu = int(menu)
                break
            print("Enter a Valid Option!")
            clean_line(2)
            menu = input("Select: ")
        players = {}
        os.system('clear')
        if menu == 1:
            pass
        elif menu == 2:
            # configure agent
            level, depth = configure_agent('White')
            players['O'] = Agent(Board.WHITE, level, depth), []
        elif menu == 3:
            level, depth = configure_agent('Black')
            players['@'] = Agent(Board.BLACK, level, depth), []
        elif menu == 4:
            level, depth = configure_agent('Black')
            players['@'] = Agent(Board.BLACK, level, depth), []
            level, depth = configure_agent('White')
            players['O'] = Agent(Board.WHITE, level, depth), []

        board = Board()
        turn = board.BLACK
        board.draw_color_board(turn)
        # Game flow
        while not board.end_of_game():
            if turn in players:  # its an agent's turn
                agent = players[turn][0]
                print(agent.color + " agent's turn")
                start = time.time()  # measure time
                move = agent.negamax_AB(turn, board, agent.depth, Agent.MIN, Agent.MAX)[1]
                end = time.time()
                players[turn][1].append(end-start)
            else:  # user turn
                while True:
                    move = input(turn+"'s turn (row col)> ")
                    if not move:
                        exit_app()
                    move = tuple(valid_play(move))
                    if move and board.is_legal(move, turn):
                        board.make_move(move, turn)
                        break
                    else:
                        print("Try a valid move!")
                        clean_line(2)
            board.make_move(move, turn)
            os.system('clear')
            prev_turn = turn
            turn = board.next_turn(turn)
            board.draw_color_board(turn)
            print(prev_turn+"'s move", move)
        print("Game Over!\n")
        for player in players:
            print("Player %s avg = %dms, max = %dms" % (player, sum(players[player][1]) * 1000 / len(players[player][1]), max(players[player][1]) * 1000))
        new_game = input("Play again? [y/n]:")
        while True:
            if new_game is 'y':
                break
            if new_game is 'n' or new_game is '':
                exit_app()
            print("Try a valid option!")
            clean_line(2)
            new_game = input("Play again? [y/n]: ")

