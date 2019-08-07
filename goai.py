from gogame.board import *
from gogame.model import *
from gogame.utils import *
from gogame.scoring import * 
from gobots.naive import *

print("There y'a GO!")

def main():
    size = 9
    game = GameState.new_game(9)
    bots = {
        Player.white: RandomBot(),
        Player.black: RandomBot()
    }
    while not game.won():
        time.sleep(0.3)
        print(chr(27) + "[2J")                           
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        print(game_result(game))
        game = game.apply_move(bot_move)

if __name__ == '__main__':
    main()