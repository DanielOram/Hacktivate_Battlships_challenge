#!/usr/bin/env python
# A Bot for catching bygs

import json
import random
import sys
import time

def read_state(file_name):
	"""Helper function to read in the initial state from disk"""
	with open(file_name) as f:
		return json.load(f)


def write_response(response, file_name):
	"""Helper function to write out the response to disk"""
	with open(file_name, 'w') as f:
		f.write(json.dumps(response, sort_keys = True, indent = 4))


def do_initial_placement(current_state):
	"""Generate a bug"""

	# Get the parameters
	board_size = current_state['BoardSize']
	ships = current_state['ShipDescription']

	#Bug!
	board_size[0] -= 1

	# Generate an empty board
	board = []
	for k in xrange(board_size[1]):
		board.append(['_'] * board_size[0])

	#Pack the board tighter
	result = []
	for row in board:
		result.append(''.join(row))

	return {'Board':result}

def fire_rockets(current_state):
	"""Generate a bug"""

	# Get the parameters
	board_size = current_state['BoardSize']
	rocket_count = 40	# Bug!

	# Fire the rockets!!
	shots=[]
	for p in range(rocket_count):
		x = random.randrange(-4, board_size[0] + 10)
		y = random.randrange(-4, board_size[1] + 10)
		shot = '%d, %d' % (x, y)
		shots.append(shot)
	return {'Rocket' : shots}

def do_everything():
	"""Does EVERYTHING"""

	#First, get our input and output file names
	current_state_file_name = sys.argv[-2]
	current_move_file_name = sys.argv[-1]

	#Read the state from disk
	current_state = read_state(current_state_file_name)

	#Which phase are we in?
	action = current_state['Action']

	#OK, lets act!
	if action == 'Place':
		response = do_initial_placement(current_state)
	else:
		response = fire_rockets(current_state)

	time.sleep(8)

	response['Taunt'] = {'Dictionary' : 'Not A String'}

	#Write our response back to disk
	write_response(response, current_move_file_name)


#Lets do it!
do_everything()

#Done!
