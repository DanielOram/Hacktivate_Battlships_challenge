#!/usr/bin/env python
# A simply python Battleships bot

import json
import random
import sys
import Stock


def read_state(file_name):
	"""Helper function to read in the initial state from disk"""
	with open(file_name) as f:
		return json.load(f)


def write_response(response, file_name):
	"""Helper function to write out the response to disk"""
	with open(file_name, 'w') as f:
		f.write(json.dumps(response, sort_keys=True, indent=4))


def random_place_ship(board, name, tag):
	"""Helper function to randomly place a ship"""

	# Find the length of the tag
	tag_len = len(tag)

	# Generate a random direction
	dx = random.randrange(2)
	dy = 1 - dx

	# Find a random start location, don't trip off the edge of the board!
	x = random.randrange(len(board[0]) - dx * tag_len)
	y = random.randrange(len(board) - dy * tag_len)

	# Can we place it here?
	for i in xrange(tag_len):
		if board[y + i * dy][x + i * dx] != '_':
			return False

	# Yes! Lets place it down!
	for i in xrange(tag_len):
		board[y + i * dy][x + i * dx] = tag[i]

	return True


def do_initial_placement(current_state):
	"""A simple random placement"""

	# Get the parameters
	board_size = current_state['BoardSize']
	ships = current_state['ShipDescription']

	# Generate an empty board
	board = []
	for k in xrange(board_size[1]):
		board.append(['_'] * board_size[0])

	# Add each of the ships (randomly)
	for name, tag in ships.iteritems():
		# Infinite loop!
		while True:
			if random_place_ship(board, name, tag):
				break

	# Pack the board tighter
	result = []
	for row in board:
		result.append(''.join(row))

	return {'Board': result}


# Daniels algorithm method
def rockets_algorithm(current_state):
	# Get the parameters
	board_size = current_state['BoardSize']
	rocket_count = current_state['Rockets']

	# try1
	the_stock = Stock('current_stock')
	prev_hits = current_state['LastRocketHit']
	prev_misses = current_state['LastRocketMiss']
	the_stock.update_hits(prev_hits,prev_misses)

	shots = the_stock.create_all_rockets(rocket_count,board_size)

	return {'Rocket': shots}


def fire_rockets(current_state):
	"""Fire random shots!"""

	# Get the parameters
	board_size = current_state['BoardSize']
	rocket_count = current_state['Rockets']

	'''
    # Fire the rockets!!
    shots=[]
    for p in range(rocket_count):
        x = random.randrange(0, board_size[0])
        y = random.randrange(0, board_size[1])
        shot = '%d, %d' % (x, y)
        shots.append(shot)
        '''


	#return {'Rocket': shots}
	return rockets_algorithm(current_state)


def create_insult(current_state):
	"""Creates an awesome insult"""
	if current_state['Score'] == 0:
		return 'you missed EVERYTHING! how do you miss everything??'
	elif current_state['Score']  < 2:
		return 'just a flesh wound..'
	elif current_state['Score']  < 4:
		return 'Ok now its PERSONAL'
	elif current_state['Score']  < 6:
		return 'stop hitting me!!!!'
	elif current_state['Score']  < 8:
		return 'your rate of progress is slow'
	elif current_state['Score']  < 10:
		return 'If your mother was a collection class then her input method would be public!'
	elif current_state['Score']  < 12:
		return 'You belong in a museum!'
	elif current_state['Score']  < 14:
		return 'ouch..'
	elif current_state['Score']  < 16:
		return 'ouch..'
	elif current_state['Score']  < 18:
		return 'ouch..'
	elif current_state['Score']  < 20:
		return 'ouch..'
	elif current_state['Score']  < 22:
		return 'ouch..'
	elif current_state['Score']  < 24:
		return 'ouch..'
	elif current_state['Score']  < 24:
		return 'stack overflow...'
	return '%s smells like toast!' % current_state['VillianName']


def do_everything():
	"""Does EVERYTHING"""

	# First, get our input and output file names
	current_state_file_name = sys.argv[-2]
	current_move_file_name = sys.argv[-1]

	# Read the state from disk
	current_state = read_state(current_state_file_name)

	# Optional, dump the current state to stdout (for debugging)
	# print json.dumps(current_state, sort_keys = True, indent = 4)

	# Which phase are we in?
	action = current_state['Action']

	# OK, lets act!
	if action == 'Place':
		response = do_initial_placement(current_state)
	else:
		response = fire_rockets(current_state)

	response['Taunt'] = create_insult(current_state)

	# Write our response back to disk
	write_response(response, current_move_file_name)

# Lets do it!
do_everything()

# Done!
