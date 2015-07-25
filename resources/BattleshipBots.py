#!/usr/bin/env python
# A Bot game of Battleships
# See License.txt for licensing details

import os
import shutil
import sys

sys.path.insert(0, './Source')

from Support import *
from Runner import play_game

#==========================================================


def show_banner():
    print_seperator()
    print "Let's play Battleships!"

    print '\nUsage:'
    print ' %s --readme' % sys.argv[0]
    print ' %s --debug <BotName> <BotName>' % sys.argv[0]
    print ' %s --play <BotName> <BotName> [UIColorA] [UIColorB]' % sys.argv[0]

    botNames = []
    for bot in os.listdir('Bots'):
        if bot[0] != '.':
            botNames.append(bot)

    print '\nAvailable Bots:'
    for bot in botNames:
        print ' *  %s' % bot

    print '\nExample:'
    print ' %s --play %s %s BLUE RED' % tuple([sys.argv[0]] + botNames[:2])

#==========================================================


def print_readme():
    with open('README.md') as f:
        print f.read()

#==========================================================
if '-r' in sys.argv or '--readme' in sys.argv:
    print_readme()
    sys.exit()

if '-d' in sys.argv or '--debug' in sys.argv:
    play_game(debug_mode=True)
    sys.exit()

if '-p' in sys.argv or '--play' in sys.argv:
    play_game(debug_mode=False)
    sys.exit()

show_banner()
