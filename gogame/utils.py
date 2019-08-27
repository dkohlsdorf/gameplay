from gogame.model import *


COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None:         '.',
    Player.black: 'x',
    Player.white: 'o'
}

def coords_from_point(point):
    return '%s%d' % (
        COLS[point.col - 1],
        point.row
    )

def print_move(player, move):
    if move.passed:
        move_str = 'pass'
    elif move.resigned:
        move_str = 'resign'
    else:
        c = COLS[move.pos.col - 1]
        r = move.pos.row
        move_str = "{}{}".format(c, r)
    print('%s %s' % (player, move_str))

def print_board(board):
    for row in range(board.rows, 0, -1):
        offset = " " if row <= 9 else ""
        line = []
        for col in range(1, board.cols + 1):
            stone = board.get_color(BoardPosition(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (offset, row, ''.join(line)))
    print('   ' + ''.join(COLS[:board.cols]))


