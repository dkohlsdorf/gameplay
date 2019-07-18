import random
import time

from gobots.agent import *
from gogame.board import *
from gogame.model import *

class RandomBot(Agent):

    def select_move(self, game_state):
        candidates = []
        for r in range(1, game_state.board.rows + 1):
            for c in range(1, game_state.board.cols + 1):
                candidate = BoardPosition(row = r, col = c)
                valid     = game_state.is_valid(Move.play(candidate))
                eye       = game_state.board.is_eye(candidate, game_state.next_player)
                if valid and not eye:
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))
