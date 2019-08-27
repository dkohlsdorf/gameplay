import enum

from collections import namedtuple
from gogame.model import BoardPosition, Player

KOMI = 0.0 #7.5

class GameResult(namedtuple('GameResult', 'b w komi')):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white

    @property
    def winning_margin(self):
        w = self.w + self.komi
        return abs(self.b - w)

    def __str__(self):        
        w = self.w + self.komi
        if self.b > w:
            return 'B+%.1f' % (self.b - w,)
        return 'W+%.1f' % (w - self.b,)


class Lable(enum.Enum):
    black = 1
    white = 2
    white_territory = 3
    black_territory = 4
    dame = 5


class TerritoryScoring:

    def __init__(self, territory_map):
        self.black_stones    = 0
        self.white_stones    = 0
        self.black_territory = 0
        self.white_territory = 0
        self.dame            = 0
        for point, status in territory_map.items():
            if status == Lable.black:
                self.black_stones += 1
            elif status == Lable.white:
                self.white_stones += 1
            elif status == Lable.black_territory:
                self.black_territory += 1
            elif status == Lable.white_territory:
                self.white_territory += 1
            elif status == Lable.dame:
                self.dame += 1



def collect_region(start_pos, board, visited={}):
    if start_pos in visited:
        return [], set()
    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    center_color = board.get_color(start_pos)   
    for neighbor in start_pos.neighbors():
        if not board.on_grid(neighbor):
            continue
        neighbor_color = board.get_color(neighbor)
        if neighbor_color == center_color:
            points, borders = collect_region(neighbor, board, visited)
            all_points  += points
            all_borders |= borders
        else:
            all_borders.add(neighbor_color)
    return all_points, all_borders


def evalualate(board):
    status = {}
    for r in range(1, board.rows + 1):
        for c in range(1, board.cols + 1):
            p = BoardPosition(r, c)
            if p in status:
                continue
            stone = board.get_color(p)
            if stone is not None:
                if stone == Player.white:
                    status[p] = Lable.white
                else:
                    status[p] = Lable.black
            else:
                group, neighbors = collect_region(p, board)                
                if len(neighbors) == 1:
                    neighbor = neighbors.pop()
                    if neighbor == Player.white:
                        fill_with = Lable.white_territory
                    else:
                        fill_with = Lable.black_territory
                else:
                    fill_with = Lable.dame
                for pos in group:
                    status[pos] = fill_with
    return TerritoryScoring(status)

def game_result(state):
    territory = evalualate(state.board)
    return GameResult(
        territory.black_territory + territory.black_stones,
        territory.white_territory + territory.white_stones,
        komi = KOMI
    )