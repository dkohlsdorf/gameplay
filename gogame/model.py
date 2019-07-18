'''
Model for the Game of GO

REFERENCE: 
  Pumperla, Furguson: "Deep Learning And The Game Of Go", Manning, 2019
'''

import enum
from collections import namedtuple

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        if self == Player.white:
            return Player.black
        else:
            return Player.white

        
class BoardPosition(namedtuple('Point', 'row col')):

    def neighbors(self):
        return [
            BoardPosition(self.row - 1, self.col    ),
            BoardPosition(self.row + 1, self.col    ),
            BoardPosition(self.row    , self.col - 1),
            BoardPosition(self.row    , self.col + 1)          
        ]

    def corners(self):
        return [
            BoardPosition(self.row - 1, self.col - 1),
            BoardPosition(self.row - 1, self.col + 1),
            BoardPosition(self.row + 1, self.col - 1),
            BoardPosition(self.row + 1, self.col + 1)
        ]



class Region:

    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, pos):
        self.liberties.remove(pos)

    def add_liberty(self, pos):
        self.liberties.add(pos)

    def merge(self, other):
        assert other.color == self.color
        color     = self.color
        stones    = self.stones | other.stones
        liberties = (self.liberties | other.liberties) - stones
        return Region(color, stones, liberties)

    @property
    def n_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        is_region      = isinstance(other, Region)
        same_color     = self.color     == other.color
        same_stones    = self.stones    == other.stones
        same_liberties = self.liberties == other.liberties 
        return is_region and same_color and same_stones and same_liberties

    
