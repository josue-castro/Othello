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
    level_option = ['0', '1', '2', '3', '4', '']
    print("DEFAULT=1".rjust(40), flush=True, end='\r')
    level = input("%s's difficulty (0-4): " % color)
    while level not in level_option:
        print("Try a Valid Option!")
        clean_line(2)
        level = input("%s's difficulty (0-4): " % color)
    level = DEFAULT_LEVEL if level is '' else int(level)

    depth_options = ['1', '2', '3', '4', '5', '6', '']
    print("DEFAULT=2".rjust(40), flush=True, end='\r')
    depth = input("%s's depth (1-6): " % color)
    while depth not in depth_options:
        print("Try a Valid Option!")
        clean_line(2)
        depth = input("%s's depth (1-6): " % color)
    depth = DEFAULT_DEPTH if depth is '' else int(depth)
    os.system('clear')
    return level, depth


if __name__ == '__main__':
    while True:
        # HEADER
        print(Back.CYAN)
        os.system('clear')
        say("Othello", font='block', align='center', colors=['white', 'black'])
        print(Fore.BLACK)
        # MENU
        print("1. Player vs Player\n2. Player vs AI\n3. AI vs Player\n4. AI vs AI\n")
        menu_options = ['1', '2', '3', '4']
        print("\t\tPress ENTER to Exit", flush=True, end='\r')
        menu = input("Select: ")
        # INPUT OPTION
        while menu not in menu_options:
            if not menu:
                exit_app()
            print("Enter a Valid Option!")
            clean_line(2)
            menu = input("Select: ")
        # VALID OPTION
        menu = int(menu)
        players = {}
        os.system('clear')
        # AGENT CONFIGURATION
        if menu == 1:
            pass
        elif menu == 2:
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
        # BEGIN GAME, SET UP BOARD
        board = Board()
        turn = board.BLACK
        board.draw_color_board(turn)
        while turn:
            # AGENT TURN
            if turn in players:
                agent = players[turn][0]
                # TIME STATISTICS
                start = time.time()
                move = agent.best_move(board)
                end = time.time()
                # ---------------
                print(agent.color + " agent's turn: ", move)
                # SAVE TIME
                players[turn][1].append(end-start)
            else:
                # USER TURN
                while True:
                    move = input(turn+"'s turn (row col)> ")
                    if not move:
                        exit_app()
                    move = tuple(valid_play(move))
                    if move and board.is_legal(move, turn):
                        break
                    else:
                        print("Try a valid move!")
                        clean_line(2)
            board.make_move(move, turn)
            os.system('clear')
            # PREPARE NEXT TURN
            prev_turn = turn
            turn = board.next_turn(turn)  # NONE IF GAME IS OVER
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

