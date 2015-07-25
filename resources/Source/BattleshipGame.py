# A Battleship Game
# See License.txt for licensing details

# This is just the module, look at ../BattleshipBots.py instead

import json
import logging
import os
import random
import shutil
import sys
import threading
import time

from Support import *

class BattleshipGame:

    def __init__(self, bot_names, bot_colors, debug_mode):
        self.debug_mode = debug_mode

        self.use_virtual_box = False

        use_big_rules = True

        if use_big_rules:
            self.board_size = [40, 40]
            self.starting_ships = {
                'Destroyer1': '22',
                'Cruiser1': '333',
                'Submarine1': '333',
                'Battleship1': '4444',
                'Carrier1': '55555',
                'Destroyer2': '22',
                'Cruiser2': '333',
                'Submarine2': '333',
                'Battleship2': '4444',
                'Carrier2': '55555'
            }
        else:
            self.board_size = [10, 10]
            self.starting_ships = {
                'Destroyer': '22',
                'Cruiser': '333',
                'Submarine': '333',
                'Battleship': '4444',
                'Carrier': '55555'
            }


        self.vboxmanage = '\"C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage\" '
        # Download virtual box from here : https://www.virtualbox.org/wiki/Downloads
        # Download a virtualbox image from here :
        # http://www.osboxes.org/ubuntu/

        self.move_number = 1

        self.board = [get_empty_board(self.board_size)] * 2

        self.bot_colors = bot_colors
        self.bot_names = bot_names
        self.bot_handle = bot_names
        if bot_names[0] == bot_names[1]:
            self.bot_handle = [bot_names[0] + '_A', bot_names[1] + '_B']

        self.last_rocket = [[], []]
        self.last_rocket_hit = [[], []]
        self.last_rocket_miss = [[], []]
        self.ships = [None, None]
        self.last_taunt = [None, None]
        self.rocket_count = [0, 0]

        self.scores = [0, 0]
        self.points_per_rocket_hit = 2
        self.points_per_ship_destroyed = 5

        destroy_and_create_empty_folder(get_livedata_dir_name())
        secret_dir_name = get_secret_dir_name()
        destroy_and_create_empty_folder(secret_dir_name)

        if self.use_virtual_box:
            for player_number in range(2):
                sandbox_name = 'Sandbox' + 'AB'[player_number]
                # Shut down the VM
                cmd = self.vboxmanage
                cmd += 'controlvm '
                cmd += sandbox_name
                cmd += ' poweroff soft '
                os.system(cmd)
            time.sleep(3)

        for player_number in range(2):
            sourceFolder = 'Bots/' + self.bot_names[player_number]
            if not os.path.isdir(sourceFolder):
                print 'Unable to find bot %s\n' % sourceFolder
                sys.exit()

            sandbox_name = 'Sandbox' + 'AB'[player_number]

            if self.use_virtual_box:
                # Unmount the shared folder
                cmd = self.vboxmanage
                cmd += 'sharedfolder '
                cmd += 'remove '
                cmd += sandbox_name
                cmd += ' --name Sandbox '
                os.system(cmd)

            # Copy in the bot
            destFolder = self.get_sandbox_dir_name(player_number)
            shutil.rmtree(destFolder, ignore_errors=True)
            shutil.copytree(sourceFolder, destFolder)

            if self.use_virtual_box:
                # Mount the shared folder
                cmd = self.vboxmanage
                cmd += 'sharedfolder '
                cmd += 'add '
                cmd += sandbox_name
                cmd += ' --name Sandbox '
                cmd += '--hostpath ' + \
                    os.getcwd() + '\\' + \
                    self.get_sandbox_dir_name(player_number).replace('/', '\\')
                cmd += ' --automount'
                cmd = cmd.replace('\\.\\', '\\')
                os.system(cmd)

                # Start the VM
                cmd = self.vboxmanage
                cmd += 'startvm '
                cmd += sandbox_name
                print cmd
                os.system(cmd)

        if self.use_virtual_box:
            # Give the VM time to boot
            time.sleep(20)

        print_seperator()

    def get_sandbox_dir_name(self, player_number):
        result = get_livedata_dir_name() + 'SandBox'
        result += self.bot_handle[player_number]
        return result

    def is_game_over(self):
        if self.move_number < 2:
            return False
        if self.is_dead(0):
            return True
        if self.is_dead(1):
            return True
        return False

    def is_dead(self, player_number):
        return (self.count_live_ships(player_number) == 0)

    def get_ship_state(self, ship, player_number):
        board = self.board[player_number]
        for t in ship['Body']:
            cell = board[t[1]][t[0]]
            if cell == ship['Flavour'][0]:
                return 'Live'
        return 'Dead'

    def count_live_ships(self, player_number):
        result = 0
        ships = self.ships[player_number]
        if not ships:
            return 0
        for ship in ships:
            if self.get_ship_state(ship, player_number) == 'Live':
                result += 1

        return result

    def get_board_state(self, player_number, fog_of_war):
        state = dict()

        state['Board'] = self.board[player_number]

        ship_count = self.count_live_ships(player_number)

        if fog_of_war:
            board = []
            for r in self.board[player_number]:
                row = ''
                for s in r:
                    if s in '123456789':
                        s = '_'
                    row += s

                board.append(row)

            state['Board'] = board
        else:
            state['Ships'] = self.ships[player_number]
            if state['Ships'] is not None:
                for ship in state['Ships']:
                    ship['LastState'] = ship.get('State','Live')
                    ship['State'] = self.get_ship_state(ship, player_number)
            state['LiveShipCount'] = ship_count

        state['BoardSize'] = self.board_size
        state['MoveNumber'] = self.move_number
        state['Score'] = self.scores[player_number]
        state['HeroName'] = self.bot_handle[player_number]
        state['HeroColor'] = self.bot_colors[player_number]
        state['VillianName'] = self.bot_handle[1 - player_number]
        state['VillianColor'] = self.bot_colors[1 - player_number]
        if self.last_taunt[player_number] is not None:
            state['VillainTaunt'] = self.last_taunt[player_number]
        state['LastRocket'] = self.last_rocket[player_number]
        state['LastRocketHit'] = self.last_rocket_hit[player_number]
        state['LastRocketMiss'] = self.last_rocket_miss[player_number]

        if self.move_number == 1:
            state['Action'] = 'Place'
            state['ShipDescription'] = self.starting_ships
        else:
            state['Action'] = 'Fire'
            self.rocket_count[player_number] = ship_count + (self.move_number - 2)
            state['Rockets'] = self.rocket_count[player_number]

        return state

    def random_place_ship_inner(self, board, name, tag):
        tag_len = len(tag)

        dx = random.randrange(2)
        dy = 1 - dx
        x = random.randrange(len(board[0]) - dx * tag_len)
        y = random.randrange(len(board) - dy * tag_len)

        for i in xrange(tag_len):
            if board[y + i * dy][x + i * dx] != '_':
                return False

        for i in xrange(tag_len):
            board[y + i * dy][x + i * dx] = tag[i]

        return True

    def random_place_ship(self, board, name, tag):

        # Infinite loop!
        while True:
            if self.random_place_ship_inner(board, name, tag):
                return

    def generate_random_ship_placement(self, board_size, ships):
        # Generate an empty board
        board = []
        for k in xrange(board_size[1]):
            board.append(['_'] * board_size[0])

        # Add each of the ships (randomly)
        for name, tag in ships.iteritems():
            self.random_place_ship(board, name, tag)

        result = []
        for row in board:
            result.append(''.join(row))

        return {'Board': result}

    def generate_random_shots(self, board_size, rocket_count):
        shots = []
        for p in range(rocket_count):
            x = random.randrange(board_size[0])
            y = random.randrange(board_size[1])
            shot = '%d, %d' % (x, y)
            shots.append(shot)
        return {'Rocket': shots}

    def generate_random_move(self, state, player_number):
        if state['Action'] == 'Place':
            move = self.generate_random_ship_placement(
                state['BoardSize'], state['ShipDescription'])
            self.append_taunt(move)
            return move
        if state['Action'] == 'Fire':
            move = self.generate_random_shots(
                state['BoardSize'], self.rocket_count[player_number])
            self.append_taunt(move)
            return move

    def append_taunt(self, move):
        move['Taunt'] = 'I shall be victorious!'

    def generate_default_move(self, secret_dir_name, player_number):
        sandbox_dir_name = self.get_sandbox_dir_name(player_number)
        player_name = self.bot_handle[player_number]

        state_fog = self.get_board_state(player_number, True)
        state_secret = self.get_board_state(player_number, False)
        write_json(state_fog, sandbox_dir_name + '/current_state.json')
        write_json(
            state_fog, sandbox_dir_name + '/past_state_%03d.json' % self.move_number)
        write_json(state_secret, secret_dir_name + '/botstate%s_move%03d.json' %
                   ('AB'[player_number], self.move_number))

        if self.is_game_over():
            #No default move needed
            return

        default_move = self.generate_random_move(state_secret, player_number)
        if not self.debug_mode:
            write_json(default_move, sandbox_dir_name + '/current_move.json')

        default_move_name = secret_dir_name + '/default_move_%s_%03d.json' % (player_name, self.move_number)
        write_json(default_move, default_move_name);
        self.load_move(default_move_name, player_number)

    def fire_rocket(self, rocket, player_number):
        board = self.board[player_number]
        # print 'Rocket:', rocket
        hit_record = []
        miss_record = []
        old_live_ship_count = self.count_live_ships(player_number)
        scoring_hit_count = 0
        for square in rocket:
            [x, y] = square.split(',')
            x = int(x)
            y = int(y)
            row = list(board[y])
            previous = row[x]
            updated = previous

            if previous in '012345789':
                # scoring hit!
                updated = '!'
                scoring_hit_count += self.points_per_rocket_hit
            elif previous == '_':
                updated = '#' # Miss!

            if updated == '!':
                hit_record.append((x, y))
            else:
                miss_record.append((x, y))

            row[x] = updated

            board[y] = ''.join(row)

        self.last_rocket_hit[player_number] = hit_record
        self.last_rocket_miss[player_number] = miss_record
        ship_shunk_count = old_live_ship_count - \
            self.count_live_ships(player_number)

        self.scores[
            player_number] += scoring_hit_count
        self.scores[player_number] += ship_shunk_count * \
            self.points_per_ship_destroyed

    def match_ship_dxdy(self, board, x, y, dx, dy):
        flavour = board[y][x]
        length = int(flavour)
        if length <= 0:
            return
        body = []
        for i in xrange(length):
            xx = x + i * dx
            yy = y + i * dy
            body.append((xx, yy))
            try:
                if board[yy][xx] != flavour:
                    return
            except IndexError:
                return
        ship = {'Flavour': flavour * length, 'Body': body}
        ship['Orientation'] = 'Horizontal' if dx != 0 else 'Vertical'
        return ship

    def match_ship(self, board, x, y):
        result = None
        try:
            result = self.match_ship_dxdy(board, x, y, 1, 0)
            if not result:
                result = self.match_ship_dxdy(board, x, y, 0, 1)
        except ValueError:
            pass
        return result

    def extract_ships(self, board):
        # First, pull out all the potential ships
        match = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                ship = self.match_ship(board, x, y)
                if not ship:
                    continue
                # erase the ship from the board
                for(xx, yy) in ship['Body']:
                    board[yy] = self.insert_string(board[yy], '*', xx)
                match.append(ship)

        # Then match them against the starting_ships
        # Care must be taken because multiple ships might share the same
        # flavour
        result = []
        for ship, flavour in self.starting_ships.iteritems():
            for q in xrange(len(match)):
                if match[q]['Flavour'] == flavour:
                    item = match[q]
                    del match[q]
                    item['Name'] = ship
                    result.append(item)
                    break

        return result

    def insert_string(self, source, s, index):
        return source[:index] + s + source[index + 1:]

    def apply_ships(self, board, ships):
        for ship in ships:
            for(xx, yy) in ship['Body']:
                flavour = ship['Flavour'][0]
                board[yy] = self.insert_string(board[yy], flavour, xx)
        return board

    def sandbox_execute(self, player_number, command):
        sys.stdout.flush()

        max_seconds_per_turn = 5

        if self.use_virtual_box:
            sandbox_name = 'Sandbox' + 'AB'[player_number]

            # Resume the VM
            cmd = self.vboxmanage
            cmd += 'controlvm ' + sandbox_name + ' resume'
            print cmd
            os.system(cmd)

            # Run the BOT in the sandbox == no cheating!
            cmd = self.vboxmanage
            cmd += 'guestcontrol ' + sandbox_name
            cmd += ' run --username osboxes --password osboxes.org '
            cmd += ' --timeout %d ' % (max_seconds_per_turn * 1000)
            cmd += ' -- bin/sh -c "cd /media/sf_Sandbox && ./runme"'
            print cmd
            os.system('\"' + cmd + '\"')

            # All done, pause the VM so the other bot gets 100% CPU
            cmd = self.vboxmanage
            cmd += 'controlvm ' + sandbox_name + ' pause'
            print cmd
            os.system(cmd)

        elif True:
            #Run the bot with a timeout
            print command
            sys.stdout.flush()
            thread = threading.Thread(target = os.system, args = (command,))
            thread.start()
            thread.join(max_seconds_per_turn)
            thread._Thread__stop() # Yeah, I killed it..

        else:
            os.system(command)

        sys.stdout.flush()


    def apply_move(self, player_number):
        sandbox_dir_name = self.get_sandbox_dir_name(player_number)
        if os.name == 'nt':
            command = (
                'cd ' + sandbox_dir_name + ' && ' + './RunMe.bat').replace('/', '\\')
        else:
            command = 'cd ' + sandbox_dir_name + ' && ' + './runMe'

        self.sandbox_execute(player_number, command)

        player_name = self.bot_handle[player_number]
        secret_dir_name = get_secret_dir_name()
        # print 'apply_move %s, %s' % (secret_dir_name, sandbox_dir_name)
        source_name = sandbox_dir_name + '/current_move.json'
        try:
            shutil.copy(source_name, secret_dir_name +
                    '/response_%s_%03d.json' % (player_name, self.move_number))
            shutil.copy(
                source_name, sandbox_dir_name + '/past_move_%03d.json' % (self.move_number))
        except:
            pass #no response?

        try:
    	    self.load_move(source_name, player_number)

        except:
            logging.exception('Bad Data')
            #Meh, bad data..
            pass

        self.fire_rocket(self.last_rocket[player_number], player_number)

    def load_move(self, source_name, player_number):
        print 'load %s'%source_name
        with open(source_name, 'r') as f:
            s = json.load(f)

        taunt = s.get('Taunt')
        if not isinstance(taunt, str):
            taunt = None
        self.last_taunt[1 - player_number] = taunt

        if self.move_number == 1:
            response_board = s['Board']
            if len(response_board) != self.board_size[1]:
                return
            if len(response_board[0]) != self.board_size[0]:
                return
            ships = self.extract_ships(response_board)
            if len(ships) != len(self.starting_ships):
                return

            actual_board = get_empty_board(self.board_size)
            actual_board = self.apply_ships(actual_board, ships)

            self.ships[1 - player_number] = ships
            self.board[1 - player_number] = actual_board
        else:
            rocket = s['Rocket']
            if not isinstance(rocket, list):
                return
            if len(rocket)>self.rocket_count[player_number]:
                # !!!
                return
            self.last_rocket[player_number] = rocket

    def next_move(self):
        self.move_number += 1

    def write_scores(self, secret_dir_name):
        status = 'Move: %d,  %s : %d points,  %s : %d points' % (
            self.move_number, self.bot_handle[0], self.scores[0], self.bot_handle[1], self.scores[1])
        if self.is_dead(0):
            if self.is_dead(1):
                status += '\nTIE! Everybody loses!!'
            else:
                status += '\n%s WINS!' % (self.bot_handle[0])
        elif self.is_dead(1):
            status += '\n%s WINS!' % (self.bot_handle[1])
        print status

if __name__ == "__main__":
    print 'This is the battleshipgame module, instead try running BattleshipBots.py'
