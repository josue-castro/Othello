import random as r
WHITE, BLACK, EMPTY = 'O', '@', ' '
DIRECTIONS = {  #row, col coordinates
    'UP': (-1, 0), 'DOWN': (1, 0),
    'RIGHT': (0, 1), 'LEFT': (0, -1),
    'UP_RIGHT': (-1, 1), 'UP_LEFT': (-1, -1),
    'DOWN_RIGHT': (1, 1), 'DOWN_LEFT': (1, -1)
}

SIZE = 6


def opponent(player):
    return BLACK if player is WHITE else WHITE


def new_board():
    assert SIZE % 2 == 0
    board = [[EMPTY]*SIZE for x in range(SIZE)]
    mid = (SIZE-2)//2
    board[mid][mid] = WHITE
    board[mid][SIZE-1-mid] = BLACK
    board[SIZE-1-mid][mid] = BLACK
    board[SIZE-1-mid][SIZE-1-mid] = WHITE
    return board


def in_bounds(row, col):
    return (0 <= row < SIZE) and (0 <= col < SIZE)


def find_bracket(move, direction, player, board):
    """Search in one direction if there is a bracket"""
    row, col = move
    dy, dx = direction  # direction displacement
    row += dy
    col += dx
    if not in_bounds(row, col) or board[row][col] == player:
        return None
    opp = opponent(player)
    while board[row][col] == opp:  # Opponent disks in straight line until bracket
        row += dy
        col += dx
        if not in_bounds(row, col):  # Entire board was search in the given direction, no bracket found
            return None
    return (row, col) if board[row][col] is player else None


def is_legal(move, player, board):
    """Search in all directions if a capture is made"""
    row, col = move
    if not in_bounds(row, col):
        return False
    bracket_moves = []  # Boolean list if there was a capture in a direction
    for direction in DIRECTIONS.values():
        bracket_moves.append(find_bracket(move, direction, player, board))
    return board[row][col] == EMPTY and any(bracket_moves)


def draw_board(player, board):
    draw = '    %s\n' % '   '.join(map(str, range(SIZE)))
    for row in range(SIZE):
        draw += '  +%s\n%d ' % (''.join(SIZE*(3*'-'+'+')), row)
        for col in range(SIZE):
            if is_legal((row, col), player, board):
                draw += '| . '
            else:
                draw += '| %s ' % board[row][col]
        draw += '|\n'
    draw += '  +%s\n' % ''.join(SIZE*(3*'-'+'+'))
    print(draw)


def legal_moves(player, board):
    moves = []
    for row in range(SIZE):
        for col in range(SIZE):
            move = row, col
            if is_legal(move,player,board):
                moves.append(move)
    return moves if moves else None


def make_move(move, player, board):
    row, col = move
    board[row][col] = player
    for direction in DIRECTIONS.values():
        make_flips(move, direction, player, board)
    return board


def make_flips(move, direction, player, board):
    bracket = find_bracket(move, direction, player, board)
    if bracket:
        row, col = move
        dy, dx = direction
        row += dy
        col += dx
        while row != bracket[0] or col != bracket[1]:
            board[row][col] = player
            row += dy
            col += dx


def rand_move(player, board):
    """Selects a random move for player"""
    valid_moves = legal_moves(player, board)
    return r.choice(valid_moves) if valid_moves else None


if __name__ == '__main__':
    board = new_board()
    player = BLACK
    draw_board(player, board)
    while True:
        move = [int(x) for x in input("(%s) row col > " % player).split()]
        if is_legal(move, player, board):
            make_move(move, player, board)
            player = opponent(player)
            draw_board(player, board)
            move = rand_move(player, board)
            make_move(move, player, board)
            player = opponent(player)
            draw_board(player, board)
            print("Player %s moved" % player, move)
        else:
            print("Try a valid move:", legal_moves(player, board))
