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
	write_response({'Bot Name': 'TorpedoBot','AllHits': [], 'AllMisses': []},'shots.json')

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


def get_prev_shots(shots_state):
    all_shots = shots_state['AllHits'] + shots_state['AllMisses']
    return all_shots

#this is a good method
def update_shots(current_state,shots_state):
    updated_hits = shots_state['AllHits'] + current_state['LastRocketHit']
    updated_misses = shots_state['AllMisses'] + current_state['LastRocketMiss']
    updated_shots_response = {'AllHits': updated_hits, 'AllMisses': updated_misses}
    write_response(updated_shots_response,'shots.json')

#hits is a list of hit coordinates
def target(hits):
    shots = []
    for h in hits:
        #left
        if h[0]==0:
            #top left - 2
            if h[1]==0:
                shots.append((h[0]+1, h[1]))
                shots.append((h[0], h[1]+1))
            #bottom left - 2
            elif h[1]==39:
                shots.append((h[0], h[1]-1))
                shots.append((h[0]+1, h[1]))
            #left edge - 2
            elif h[1]>0 and h[1]<39:
                shots.append((h[0], h[1]-1))
                shots.append((h[0], h[1]+1))
        #right
        if h[0]==39:
            #top right - 2
            if h[1]==0:
                shots.append((h[0]-1, h[1]))
                shots.append((h[0], h[1]+1))
            #bottom right - 2
            elif h[1]==39:
                shots.append((h[0], h[1]-1))
                shots.append((h[0]-1, h[1]))
            #right edge - 2
            elif h[1]>0 and h[1]<39:
                shots.append((h[0], h[1]-1))
                shots.append((h[0], h[1]+1))
        #top
        if h[1]==0:
            #top edge - 2
            if h[0]>0 and h[0]<39:
                shots.append((h[0]-1, h[1]))
                shots.append((h[0]+1, h[1]))
        #bottom
        if h[1]==39:
            #bottom edge
            if h[0]>0 and h[0]<39:
                shots.append((h[0]-1, h[1]))
                shots.append((h[0]+1, h[1]))
        #inner board square
        if h[0]>0 and h[0]<39 and h[1]>0 and h[1]<39:
            shots.append((h[0], h[1]-1))
            shots.append((h[0], h[1]+1))
            shots.append((h[0]-1, h[1]))
            shots.append((h[0]+1, h[1]))

    return shots


def fire_rockets(current_state,shots_state):
    """Fire random shots!"""

    # Get the parameters
    board_size = current_state['BoardSize']
    rocket_count = current_state['Rockets']

    shots = []


    #update hits and misses
    update_shots(current_state,shots_state)

    #number of hits
    hits = current_state['LastRocketHit']

    #previous shots
    prev_shots = get_prev_shots(shots_state)

    #algorithm for getting next hit
    targeted_hits = list(set(target(hits)))
    #take out invalid shots
    targeted_hits = [hit for hit in targeted_hits if hit not in prev_shots]
    convert_target = lambda t: '{0:d}, {1:d}'.format(t[0], t[1])
    list_targeted_hits = [convert_target(t) for t in targeted_hits]
    rocket_count = rocket_count-len(list_targeted_hits)
    #create random rockets
    shots = shots + list_targeted_hits
    for p in range(rocket_count):
        invalid_shot = True
        while invalid_shot:
            x = random.randrange(0, board_size[0])
            y = random.randrange(0, board_size[1])
            shot = '%d, %d' % (x, y)
            if not shot in prev_shots and not shot in targeted_hits:
                invalid_shot = False
        shots.append(shot)
    return {'Rocket' : shots}

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

    #read the shots state from file
    shots_state = read_state('shots.json')

    #OK, lets act!
    if action == 'Place':
        response = do_initial_placement(current_state)
    else:
        response = fire_rockets(current_state,shots_state)

    response['Taunt'] = create_insult(current_state)

    #Write our response back to disk
    write_response(response, current_move_file_name)


#Lets do it!
do_everything()

#Done!
