import time

from gogame.board import *
from gogame.model import *
from gogame.utils import *
from gogame.scoring import * 
from gobots.monte_carlo import *

print("There y'a GO!")

def main():
    game = GameState.new_game(5)
    bots = {
        Player.white: RandomBot(),
        Player.black: MonteCarloTreeSearchAgent(50, 1.0)
    }
    while not game.won():
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
    print(game_result(game))

if __name__ == '__main__':
    main()