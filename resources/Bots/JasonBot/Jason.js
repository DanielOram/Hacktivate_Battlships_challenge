// A simple node.js Battleships bot

function do_initial_placement(current_state)
{
	board = []
	xDim = current_state.BoardSize[0]
	yDim = current_state.BoardSize[1]
	for(y=0; y<yDim; y++)
	{
		board.push("__________")
	}

	return {'Board': board}
}

function fire_rockets(current_state)
{
	xDim = current_state.BoardSize[0]
	yDim = current_state.BoardSize[1]
	rocket_count = current_state.Rockets
	rockets = []
	for (i=0; i<rocket_count; i++)
	{
		x = Math.floor(xDim * Math.random())
		y = Math.floor(yDim * Math.random())
		rockets.push("" + x + ", " + y)
	}
	return {'Rocket': rockets}
}

function append_taunt(current_state, response)
{
	response['Taunt'] = current_state['VillianName'] + ' is very mean!'
}

// First, get our input and output file names
current_state_filename = process.argv[2]
current_move_filename = process.argv[3]

// Read in the current state
fs = require('fs')
current_state = JSON.parse(fs.readFileSync(current_state_filename))

// Optional, dump the current state for debugging
//console.log(current_state)

//Which phase are we in?
action = current_state['Action']
console.log(action)

if (action=='Place')
{
	response = do_initial_placement(current_state)
}
else
{
	response = fire_rockets(current_state)
}

append_taunt(current_state, response)

//Optional, for debugging
//console.log(response)

fs.writeFile(current_move_filename, JSON.stringify(response) )
