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


def hard_place_ship(current_state):

	board_size = current_state['BoardSize']
	ships = current_state['ShipDescription']

	board = []
	for k in xrange(board_size[1]):
		board.append(['_'] * board_size[0])


	board[38][1] = '5'
	board[38][5] = '3'
	board[38][6] = '3'
	board[38][7] = '3'
	board[38][10] = '3'
	board[38][11] = '3'
	board[38][12] = '3'
	board[38][15] = '4'
	board[38][16] = '4'
	board[38][17] = '4'
	board[38][18] = '4'
	board[38][21] = '5'
	board[38][22] = '5'
	board[38][23] = '5'
	board[38][24] = '5'
	board[38][25] = '5'
	board[38][28] = '3'
	board[38][29] = '3'
	board[38][30] = '3'
	board[38][33] = '2'
	board[38][34] = '2'
	board[38][37] = '2'
	board[38][38] = '2'

	board[37][1] = '5'
	board[36][1] = '5'
	board[35][1] = '5'
	board[34][1] = '5'

	board[36][4] = '4'
	board[35][4] = '4'
	board[34][4] = '4'
	board[33][4] = '4'

	board[35][7] = '3'
	board[35][8] = '3'
	board[35][9] = '3'

	result = []
	for row in board:
		result.append(''.join(row))

	return {'Board':result}

def random_place_ship(board, name, tag):
	"""Helper function to randomly place a ship"""

	#Find the length of the tag
	tag_len = len(tag)

	#Generate a random direction
	dx = random.randrange(2)
	dy = 1 - dx
	TopOrBottom = random.randrange(4)
	# 0 = top, 1 = right, 2 = bottom, 3 = left

	#Find a random start location, don't trip off the edge of the board!
	if TopOrBottom == 0:
		x = random.randrange(len(board[0]) - dx * tag_len - 2) + 1
		y = random.randrange(4) + 1

	elif TopOrBottom == 2:
		x = random.randrange(len(board[0]) - dx * tag_len - 2) + 1
		y = random.randrange(4) + 35

	elif TopOrBottom == 3:
		x = random.randrange(4) + 1
		y = random.randrange(len(board) - dy * tag_len - 2) + 1

	else:
		x = random.randrange(4) + 35
		y = random.randrange(len(board) - dy * tag_len - 2) + 1


	try:
		#Can we place it here?
		for i in xrange(tag_len):
			if board[y + i * dy][x + i * dx] != '_':
				return False

		#Is there a ship within 2 square?
		if dx == 0:
			#1 square?
			for i in xrange(tag_len):
				if board[y + i * dy][x - 1] != '_':
					return False
				if board[y + i * dy][x + 1] != '_':
					return False

			if board[y - 1][x] != '_' or board[y + tag_len][x] != '_':
				return False

			#2 squares?
			if x > 1 and x < 38:
				for i in xrange(tag_len):
					if board[y + i * dy][x - 2] != '_':
						return False
					if board[y + i * dy][x + 2] != '_':
						return False

				if y > 1 and y < 38:
					if board[y - 2][x] != '_' or board[y + tag_len + 1][x] != '_':
						return False

		else:
			#1 square?
			for i in xrange(tag_len):
				if board[y - 1][x + i * dy] != '_':
					return False
				if board[y + 1][x + i * dy] != '_':
					return False
			if board[y][x - 1] != '_' or board[y][x + tag_len] != '_':
				return False

			#2 squares?
			if y > 1 and y < 38:
				for i in xrange(tag_len):
					if board[y - 2][x + i * dy] != '_':
						return False
					if board[y + 2][x + i * dy] != '_':
						return False
			if x > 1 and x < 38:
				if board[y][x - 2] != '_' or board[y][x + tag_len + 1] != '_':
					return False

	except:
		return False

	#Yes! Lets place it down!
	for i in xrange(tag_len):
		board[y + i * dy][x + i * dx] = tag[i]
		if dx == 0:
			board[y + i * dy][x + 1] = 'x'
			board[y + i * dy][x - 1] = 'x'
			board[y - 1][x] = 'x'
			board[y + tag_len][x] = 'x'

		else:
			board[y + 1][x + i * dx] = 'x'
			board[y - 1][x + i * dx] = 'x'
			board[y][x - 1] = 'x'
			board[y][x + tag_len] = 'x'

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

	for i in xrange(40):
		for j in xrange(40):
			if board[i][j] == 'x':
				board[i][j] = '_'

	#Pack the board tighter
	result = []
	for row in board:
		result.append(''.join(row))

	return {'Board':result}


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

    radius = 100
    rangeX = (0, board_size[0])
    rangeY = (0, board_size[1])


    # Generate a set of all points within 200 of the origin, to be used as offsets later
    # There's probably a more efficient way to do this.
    deltas = set()
    for x in range(-radius, radius+1):
        for y in range(-radius, radius+1):
            if x*x + y*y <= radius*radius:
                deltas.add((x,y))

    randpoints = []
    excluded = set()
    i = 0

    # Fire the rockets!!
    shots=[]
    for p in range(rocket_count):
                x = random.randrange(*rangeX)
                y = random.randrange(*rangeY)
                if (x,y) in excluded:
                    continue
                randpoints.append((x,y))
                excluded.update((x+dx, y+dy) for (dx,dy) in deltas)
                shot = '%d, %d' % (x, y)
                shots.append(shot)
    return {'Rocket' : shots}


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
