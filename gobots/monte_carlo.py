
from random import randint
from gogame.model import Player
from gogame.board import Move
from gobots.agent import Agent

class Node:

    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0
            Player.white: 0
        }
        self.n_rollouts = 0
        self.children = []
        self.open = [move for move in state.valid_moves()] + [Move.pass_turn(), Move.resign()]

    def add_random_child(self):
        index   = randint(0, len(self.open))
        next_mv = self.open.pop(index)
        next_s  = self.state.apply_move(next_mv)
        node    = Node(next_s, self, next_mv)
        self.children.append(node) 
        return node

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.n_rollouts += 1

    def has_potential_children(self):
        return len(self.open) > 0

    def is_terminal(self):
        return self.state.won()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.n_rollouts)


class MonteCarloTreeSearchAgent(Agent):

    def __init__(self, n_rollouts):
        self.n_rollouts = n_rollouts

    def select_child(self, node):
        pass