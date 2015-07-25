# A Battleship Runner
# See license.txt for licensing details

import os
import shutil
import sys

import BattleshipGame

from Support import *

#==========================================================


def run_game(battle_ship_game):
    for move in xrange(21):
        print_seperator()
        secret_dir_name = get_secret_dir_name()
        battle_ship_game.generate_default_move(secret_dir_name, 0)
        battle_ship_game.generate_default_move(secret_dir_name, 1)

        if battle_ship_game.is_game_over():
            #Write out the state so we can viz better
            break

        battle_ship_game.apply_move(0)
        battle_ship_game.apply_move(1)
        battle_ship_game.next_move()
        battle_ship_game.write_scores(secret_dir_name)

#==========================================================


def collate_results(battle_ship_game):
    print_seperator()

#==========================================================


def play_game(debug_mode):
    print "Let's play Battleships!"

    bot_names = []
    bot_colors = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            continue
        color = color_from_name(arg)
        if color is None:
            bot_names.append(arg)
        else:
            bot_colors.append(color)

    if len(bot_names)==1:
        bot_names.append(bot_names[0])
    if len(bot_colors)<2:
        bot_colors.append(color_from_name('green'))
    if len(bot_colors)<2:
        bot_colors.append(color_from_name('orange'))

    battle_ship_game = BattleshipGame.BattleshipGame(bot_names, bot_colors, debug_mode)

    run_game(battle_ship_game)

    collate_results(battle_ship_game)

