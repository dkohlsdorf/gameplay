
import math

from random import randint
from gogame.model import Player
from gogame.board import Move
from gobots.agent import Agent
from gobots.naive import RandomBot


class Node:

    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0
        }
        self.n_rollouts = 0
        self.children = []
        self.open = [move for move in state.valid_moves()] + [Move.pass_turn(), Move.resign()]

    def add_random_child(self):
        index   = randint(0, len(self.open) - 1)
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

    def __init__(self, n_rollouts, temperature):
        self.n_rollouts = n_rollouts
        self.temperature = temperature

    def select_child(self, node):
        total_rollouts = sum(child.n_rollouts for child in node.children)
        log_rollouts   = math.log(total_rollouts)

        best_score = -1
        for child in node.children:
            wins        = child.winning_frac(node.state.next_player)
            exploration = math.sqrt(log_rollouts / child.num_rollouts)
            score       = wins + self.temperature * exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def select_move(self, state):
        root = Node(state)
        for i in range(self.n_rollouts):
            node = root
            while (not node.is_terminal()) and (not node.has_potential_children):
                node = self.select_child(node)
            if node.has_potential_children():
                node = node.add_random_child()
            winner = MonteCarloTreeSearchAgent.simulate(node.state)
            while node is not None:
                node.record_win(winner)
                node = node.parent
        scored = [(c.winning_frac(state.next_player), c.move, c.n_rollouts)
            for c in root.children]
        scored.sort(key=lambda x: x[0], reverse=True)
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move

    @staticmethod
    def simulate(game):
        bots = {
            Player.black: RandomBot(),
            Player.white: RandomBot()
        }
        while not game.won():
            move = bots[game.next_player].select_move(game)
            game = game.apply_move(move)
        return game.winner()