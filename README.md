![Boxed in](docs/images/boxedin_cube.png)

# Boxed In
Welcome to Boxed In! A terminal based adventure game created in [prompt-toolkit for Python](https://python-prompt-toolkit.readthedocs.io/).

# Gameplay
In Boxed In, you play the character of Bob, a teenager who finds himself to be abducted and left in the outdoors. He quickly finds out though, that his surroundings are anything but normal, and that in reality he's been trapped in a large box.

In order to escape, you'll have to think _inside_ the box because, well, you're Boxed In! You don't have a choice!

## Installation and setup
1. Clone the repository to your local machine.
2. Install the requirements listed in `requirements.txt` (it is recommended that you initialise a virtual environment for this).
3. `cd` into the `src` folder.
4. Run the game by running `python first-screen.py`

## Compatability notes:
Some people may experience issues with the `playsound` Python library.

This only occurs in the maze section of the game, and can be remedied by commenting out code from `playsound` (lines `138-153` inclusive and adding `pass` to line `137` in `src/maze.py`).



## I experienced some unexpected behaviour, is it a bug?
In the spirit of thinking inside the box, the game will punish you if you try thinking outside of the box. These punishments manifest themselves in the way of bugs! (10/10 100% intentional feature)

Hence our game is 100% bug free, and is indeed feature rich 🤩.


## Background
This game was made as a part of the [Python Discord Summer Code Jam 2021](https://pythondiscord.com/events/code-jams/8/)!
