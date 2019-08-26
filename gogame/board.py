'''
Board for the Game of GO

REFERENCE: 
  Pumperla, Furguson: "Deep Learning And The Game Of Go", Manning, 2019
'''
from gogame.model import Player, BoardPosition, Region 
from gogame.scoring import game_result
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
        
    def on_grid(self, pos):
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
        for pos in connected.stones:
            for neighbor in pos.neighbors():
                neighbor_region = self.get_connected(neighbor)
                if neighbor_region is None:
                    continue
                if neighbor_region is not connected:
                    neighbor_region.add_liberty(pos)
            self.grid[pos] = None

    def is_eye(self, pos, color):
        if self.get_color(pos) is not None:
            return False
        for neighbor in pos.neighbors():
            if self.on_grid(neighbor):
                neighbor_color = self.get_color(neighbor)
                if neighbor_color != color:
                    return False
        my_corners    = 0
        other_corners = 0
        corners = pos.corners()
        for corner in corners:
            if self.on_grid(corner):
                corner_color = self.get_color(corner)
                if corner_color == color:
                    my_corners += 1
                else:
                    other_corners += 1
        if other_corners > 0:
            return other_corners + my_corners == 4 
        return my_corners >= 3


class GameState:

    def __init__(self, board, next_player, prev, move):
        self.board = board
        self.next_player = next_player
        self.prev = prev
        self.last_move = move 
    
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place(self.next_player, move.pos)
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

    def winner(self):
        if not self.won():
            return None
        if self.last_move.resigned:
            return self.next_player
        result = game_result(self)
        return result.winner

    def is_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place(player, move.pos)
        connected = next_board.get_connected(move.pos)
        return connected.n_liberties == 0

    @property
    def situation(self):
        return self.next_player, self.board

    def violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place(player, move.pos)
        next_situation = (player.other, next_board)
        past = self.prev
        while past is not None:
            if past.situation == next_situation:
                return True
            past = past.prev
        return False

    def is_valid(self, move):
        if self.won():
            return False
        if move.passed or move.resigned:
            return True 
        return self.board.get_color(move.pos) is None and not self.is_self_capture(self.next_player, move) and not self.violate_ko(self.next_player, move)

    def valid_moves(self):
        for row in range(1, self.board.rows):
            for col in range(1, self.board.cols):
                move = Move.play(BoardPosition(row, col))
                if self.is_valid(move):
                    yield move