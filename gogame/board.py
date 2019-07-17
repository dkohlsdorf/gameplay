'''
Board for the Game of GO

REFERENCE: 
  Pumperla, Furguson: "Deep Learning And The Game Of Go", Manning, 2019
'''
from gogame.model import Player, BoardPosition, Region 

import copy 


class Move():

    def __init__(self, pos = None, passed = False, resigned = False):
        self.pos = pos
        self.passed = passed
        self.resigned = resigned
        self.is_play = self.pos is not None

    @classmethod
    def play(cls, pos):
        return Move(pos = pos)

    @classmethod
    def pass_turn(cls):
        return Move(passed = True)

    @classmethod
    def resign(cls):
        return Move(resigned = True)
    

class Board():

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = {}
    
    def place(self, player, pos):
        assert self.on_grid(pos)
        assert self.get_connected(pos) is None
        same_color  = []
        other_color = []
        liberties            = []
        for neighbor in pos.neighbors():
            if not self.on_grid(neighbor):
                continue
            connected = self.get_connected(pos)
            if connected is None:
                liberties.append(neighbor)
            elif connected.color == player.color:
                if connected not in same_color:
                    same_color.append(connected)
            else:
                if connected not in other_color:
                    other_color.append(connected)
        connected = Region(player, [pos], liberties)
        for same in same_color:
            connected = connected.merge(same)
        for stone in connected.stones:
            self.grid[stone] = connected
        for other in other_color:
            other.remove_liberty(pos)
        for other in other_color:
            if other.n_liberties == 0:
                self.remove(other)
        
    def on_grid(seld, pos):
        in_rows = 1 <= pos.row <= self.rows
        in_cols = 1 <= pos.col <= self.cols
        return in_rows and in_cols

    def get_color(self, pos):
        connected = self.get_connected(pos)
        if connected is None:
            return None
        return connected.color

    def get_connected(self, pos):
        return self.grid.get(pos)

    def remove(self, connected):
        for point in connected.stones:
            for neighbor in point.neighbors():
                neighbor_region = self.get_connected(neighbor)
                if neighbor_region is None:
                    continue
                if neighbor_region is not connected:
                    neighbor_region.add_liberty(point)
            self.grid[pos] = None


class GameState:

    def __init__(self, board, next_player, prev, move):
        self.board = board
        self.next_player = next_player
        self.prev = prev
        self.last_move = move 

    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.pos)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    def won(self):
        if self.last_move is None:
            return False
        if self.last_move.resigned:
            return True
        penultimate = self.prev.last_move
        if penultimate is None:
            return False
        return self.last_move.passed and penultimate.passed
