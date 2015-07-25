__author__ = 'danieloram'

import random
import json

class Stock:

    def read_state(file_name):
	"""Helper function to read in the initial state from disk"""
	with open(file_name) as f:
		return json.load(f)

    def write_response(response, file_name):
	"""Helper function to write out the response to disk"""
	with open(file_name, 'w') as f:
		f.write(json.dumps(response, sort_keys = True, indent = 4))

    def __init__(self,file):
        init_stock = self.read_state(file)
        self.all_hits = init_stock['AllHits']
        self.all_misses = init_stock['AllMisses']
        self.invalid_shots = init_stock['InvalidShots']

    def update_hits(self, hits, misses):
        response = {'Stock': 'Stock'}
        self.all_hits.append(hits)
        response['AllHits'] = self.all_hits
        self.all_misses.append(misses)
        response['AllMisses'] = self.all_misses
        self.invalid_shots = self.all_hits + self.all_misses
        response['InvalidShots'] = self.invalid_shots

        self.write_response(response, 'current_stock')


    def is_valid_shot(self,shot):
        if not shot in self.invalid_shots & shot[0]!=-1 & shot[1]!=-1:
            return True
        #make this recursive?


    def create_all_rockets(self, rocket_count,board_size):
        rockets = []
        shots=[]
        shot = '%d, %d' % (-1, -1)
        for p in range(rocket_count):
            while not self.is_valid_shot(shot):
                x = random.randrange(0, board_size[0])
                y = random.randrange(0, board_size[1])
                shot = '%d, %d' % (x, y)
            shots.append(shot)
        return {'Rocket' : shots}