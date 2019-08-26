import time

from gogame.board import *
from gogame.model import *
from gogame.utils import *
from gogame.scoring import * 
from gobots.monte_carlo import *

print("There y'a GO!")

def main():
    game = GameState.new_game(9)
    bots = {
        Player.white: MonteCarloTreeSearchAgent(2, 1.0),
        Player.black: MonteCarloTreeSearchAgent(2, 1.0)
    }
    while not game.won():
        #time.sleep(0.3)
        #print(chr(27) + "[2J")                           
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        print(game_result(game))
        game = game.apply_move(bot_move)
    
if __name__ == '__main__':
    main()