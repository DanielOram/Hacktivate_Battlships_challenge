#!/usr/bin/env python
# A simply python Battleships bot

import json
import random
import sys

def read_state(file_name):
	"""Helper function to read in the initial state from disk"""
	with open(file_name) as f:
		return json.load(f)


def write_response(response, file_name):
	"""Helper function to write out the response to disk"""
	with open(file_name, 'w') as f:
		f.write(json.dumps(response, sort_keys = True, indent = 4))


def random_place_ship(board, name, tag):
	"""Helper function to randomly place a ship"""

	#Find the length of the tag
	tag_len = len(tag)

	#Generate a random direction
	dx = random.randrange(2)
	dy = 1 - dx

	#Find a random start location, don't trip off the edge of the board!
	x = random.randrange(len(board[0]) - dx * tag_len)
	y = random.randrange(len(board) - dy * tag_len)

	#Can we place it here?
	for i in xrange(tag_len):
		if board[y + i * dy][x + i * dx] != '_':
			return False

	#Yes! Lets place it down!
	for i in xrange(tag_len):
		board[y + i * dy][x + i * dx] = tag[i]

	return True


def do_initial_placement(current_state):
	"""A simple random placement"""

	#create shots.json file
	write_response({'AllHits': [-1,-1], 'AllMisses': [-1,-1]},'shots')

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

	#Pack the board tighter
	result = []
	for row in board:
		result.append(''.join(row))

	return {'Board':result}

def get_prev_shots():
	shot_json = read_state('shots')
	all_hits = shot_json['AllHits']
	all_misses = shot_json['AllMisses']
	all_shots = all_hits + all_misses
	return all_shots


def create_all_rockets(rocket_count,board_size):
	print("debug")
	prev_shots = get_prev_shots()
	print("debug1")
	shots=[]
	x = random.randrange(0, board_size[0])
	y = random.randrange(0, board_size[1])
	shot = '%d, %d' % (x, y)
	print('debug2')
	#problem here with the code taking more than 5 seconds!! wtf!!
	for p in range(rocket_count):
		while not shot in prev_shots:
			x = random.randrange(0, board_size[0])
			y = random.randrange(0, board_size[1])
			shot = '%d, %d' % (x, y)
		shots.append(shot)
	print("debug3")
	return {'Rocket' : shots}

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

	return {'Rocket' : shots}
	'''
	return create_all_rockets(rocket_count,board_size)

def create_insult(current_state):
	"""Creates an awesome insult"""
	return '%s smells like toast!' % current_state['VillianName']

def do_everything():
	"""Does EVERYTHING"""

	#First, get our input and output file names
	current_state_file_name = sys.argv[-2]
	current_move_file_name = sys.argv[-1]

	#Read the state from disk
	current_state = read_state(current_state_file_name)

	#Optional, dump the current state to stdout (for debugging)
	#print json.dumps(current_state, sort_keys = True, indent = 4)

	#Which phase are we in?
	action = current_state['Action']

	#OK, lets act!
	if action == 'Place':
		response = do_initial_placement(current_state)
	else:
		response = fire_rockets(current_state)

	response['Taunt'] = create_insult(current_state)

	#Write our response back to disk
	write_response(response, current_move_file_name)


#Lets do it!
do_everything()

#Done!
