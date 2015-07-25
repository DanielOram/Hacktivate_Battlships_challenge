# BATTLESHIP BOTS #

Welcome, Commander, to Battleship Bots!

Your mission is to write an AI to blow the enemy out of the water!



## THE RULES ##

The rules of Battleship are simple!

Two AI bots face off in a battle to the death.

Each bot gets a 40x40 board to place their ships.

Here is your board:

    "Board": [
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________"
    ], 
	"BoardSize": [
		40, 
		40
	] 

You have 10 ships to place down. Here are your ships:

	{
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

You can choose to place your ships either horizontally or vertically, but remember, they must remain on the board at all times. Here's what a board looks like, with ships!

    "Board": [
        "________________________________________", 
        "________________________________________", 
        "__________________________________3_____", 
        "__________________________________3_____", 
        "____________________________4_____3_____", 
        "____________________________4___________", 
        "____________________________4___________", 
        "____________________________4___________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "______________________________2_________", 
        "______________________________2_________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "______333_______________________________", 
        "____________5___________________5_______", 
        "____________5___________________5_______", 
        "____________5___________________5_____3_", 
        "____________5___________________5_____3_", 
        "____________5___________________5_____3_", 
        "_______________________________________4", 
        "___________________3___________________4", 
        "___________________3___________________4", 
        "___________________3___________________4", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "___________________2____________________", 
        "___________________2____________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________"
    ], 

## Rockets ##

Rockets are awesome. For a bot, this is what 10 rockets looks like:

    "Rocket": [
        "21, 4", 
        "15, 26", 
        "38, 39", 
        "34, 26", 
        "24, 36", 
        "17, 14", 
        "7, 35", 
        "14, 33", 
        "15, 31", 
        "28, 5"
    ]

And here's the damage they can do:

    "Board": [
        "________________________________________", 
        "________________________________________", 
        "__________________________________3_____", 
        "__________________________________3_____", 
        "_____________________#______4_____3_____", 
        "____________________________!___________", 
        "____________________________4___________", 
        "____________________________4___________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "______________________________2_________", 
        "______________________________2_________", 
        "_________________#______________________", 
        "________________________________________", 
        "________________________________________", 
        "______333_______________________________", 
        "____________5___________________5_______", 
        "____________5___________________5_______", 
        "____________5___________________5_____3_", 
        "____________5___________________5_____3_", 
        "____________5___________________5_____3_", 
        "_______________________________________4", 
        "___________________3___________________4", 
        "___________________3___________________4", 
        "_______________#___3______________#____4", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "________________________________________", 
        "_______________#________________________", 
        "________________________________________", 
        "______________#_________________________", 
        "___________________2____________________", 
        "_______#___________2____________________", 
        "________________________#_______________", 
        "________________________________________", 
        "________________________________________", 
        "______________________________________#_"
    ], 

`"0, 0"` is the top left  
`"39, 0"` is the top right  
`"39, 39"` is the bottom right  

`#` is a miss  

`!` is a hit! 

All of this data is recorded in the LiveData/Secret folder.

## `"Action": "Place"` your ships! ##

On your first move, your bot will place your ships on the board.

## `"Action": "Fire"` your rockets! ###

On each subsequent move, you'll get to fire your rockets

You get to fire one rocket for each ship still alive.

You'll receive an extra bonus rocket for each round you stay alive.

For example, if you've been firing for 10 rounds, and you have 3 ships still alive, your bot can fire 10 + 3 = 13 rockets!

## Scoring ##

How do you get points? By crushing your enemy!

* 2 Points for every hit.
* 5 Points when you destroy an enemy ship.

You will get 20 moves to inflict as much damage as possible.
The bot with the most points is the winner! There is no second place.

## Cheating ##

Commander! **There is no cheating in this tournament!** If your bot crashes, or makes an illegal move, or fails to make a move, or takes too long to make a move, a default move will be generated for you!

In fact, that default move that will be supplied to you, is called `current_move.json`.

And don't think you can just fill up the hard drive, or snoop around and try to find the other bot, or use the network to access the secret information. We thought of all those things already Commander! That's why your bot will be running in a sandbox. See below for all the gory details. 

## Taunts ##

Does your bot think it's pretty awesome? **Bots absolutely hate it when you antropomorphise them.** Why not throw in some taunts to unnerve your opponent:

    "Taunt": "Less QQ, More Pew Pew!"

----------


# Lets get started! #

Commander, will you accept this challenge? 

* Clone this repo
* Are you running on Windows? You will need to install [Python 2.7](https://www.python.org/downloads)
* Run the makefile (`make`), or run `BattleshipBots.py` directly to read these rules of the game
* Lets play! Match two bots by running:

    BattleshipBots.py --play MontyBot KRBot


## Making a new Bot ##

Look in the `Bots` folder and choose a starting bot to customise:

* **KRBot** (written in your choice of **C** or **C++**)
* **JasonBot** (written in **node.js**)
* **MontyBot** (written in **Python**)

* **SpiderBot** (Don't choose this one, it's just for catching bugs)

* **LazyBot** (Empty! Create your own from a blank slate!)

Think up an awesome name for your bot, copy the existing folder, and rename it.
Now set to work firing those rockets.

To run your bot, simply use the following command

    .\BattleshipBots.py --play LazyBot <YOUR BOT NAME HERE>

This will play a complete game of Battleships, copying an audit trail of the entire
game into the `LiveData/Secret` folder.

When developing your bot, you may find it convenient to stop the action
whenever your bot fails to output a move.  Try this command:

    .\BattleshipBots.py --debug LazyBot <YOUR BOT NAME HERE>

Feel free to modify the Makefile, or even the Source folder,
to make it easier to develop your bot.

## Make your move ##

Each time your bot has an opportunity to move, the batch file `runme` (MacOS/linux) or `RunMe.bat` (Windows) will be executed.

The current game state (as visible by your bot) will be available in a JSON file called `current_state.json`.

Modify the batch file to invoke your bot. You can use any language you like, so long as you stay inside the sandbox environment.

When you've decided upon your move, simply write it out to the file `current_move.json`, and return from the batch script.

Here's a simple valid move, firing 2 rockets:

	{
	    "Rocket": [
	        "9, 6", 
	        "7, 8"
	    ]
	}

You can check your json at [http://jsonlint.org](http://jsonlint.org/ "jsonlint.org")

You'll get 5 seconds to make your move.


## Deployment ##

Your bot will run in a sandboxed environment, e.g. [VirtualBox](https://www.virtualbox.org/ "VirtualBox")

We'll work with you to install any libraries or modules or runtimes that you might need
to get your bot running in the sandbox environment.

Remember, **Once the tournament has started, the virtual network adapter inside the sandbox
will be disabled.**

In more detail, your goal is to write an AI which wins at the game of Battleships.
Attempting to escape the sandbox VM or obtain information from outside
the SandBox folder may result in disqualification from the tournament.

(You are welcome to try and generate badly formed response JSON,
but probably we'll modify the host environment to protect against it.)

## Links and Tips ##
* For all things JSON related: [json.org](http://json.org "JSON.org")

* More things JSON related: [http://jsonlint.org](http://jsonlint.org/ "jsonlint.org")
