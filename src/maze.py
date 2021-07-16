import pygments
import pygments.lexers
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import (
    Float, FloatContainer, HSplit, Window, WindowAlign
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame

from random import shuffle, randrange, randint
import typing
from typing import Literal
import entities
import numpy as np
from person import Person

class Maze:
    '''
    A class that randomly generates a maze with a set width and height.
    It can be represented in text(cells) and numpy array form(rows)
    '''
    
    # Initialize values of the maze object
    def __init__(self, width:int, height:int, num_keys:int, scale: int=1) -> None:
        self.height: int = height
        self.width: int = width
        self.num_keys: int = num_keys
        self.scale = scale
        self.true_width: int = self.width*(1+self.scale*2)+1
        self.true_height: int = self.height*(1+self.scale)+1
        self.cells = []
        self.bare = []
        self.create_maze()
        self.rows = self.make_lines()
        spawn_and_keys = self.spawn_and_key()
        self.player_pos = spawn_and_keys[0]
        self.key_pos = spawn_and_keys[1]
        self.rows = self.make_lines()
        self.keys_collected = 0
        
    def check(self, direction: typing.Literal["left", "up", "down", "right"]) -> bool:
        """Checks whether the user specified point is blank or not
        :type entity: object, imported from entities.py
        :param direction : The direction in which you want to check
        :return: A boolean object.
        """
        player_pos = self.player_pos
        if direction == "left":
            user_point = self.rows[
                         player_pos[0]:player_pos[0] + 1, player_pos[1] - 1:player_pos[1]
                         ]
        elif direction == "right":
            user_point = self.rows[player_pos[0]:player_pos[0] + 1,
                                       player_pos[1] + 1:player_pos[1] + 1 + 1]

        elif direction == "up":
            user_point = self.rows[
                         player_pos[0] - 1:player_pos[0], player_pos[1] :player_pos[1] + 1
                         ]
        else:
            # also could be written as elif direction == "down".
            user_point = self.rows[player_pos[0]+ 1:player_pos[0] + 1 + 1,
                                       player_pos[1]:player_pos[1] + 1]

        if np.all(user_point == 0):
            # Checks if the point is empty, if yes it returns True if no then it returns False.
            return True
        else:
            return False

    # Create and display the maze, creates the cells attribute
    def create_maze(self) -> None:
        h: int = self.height
        w: int = self.width
        # Keep track of the cells that have already been explored
        seen = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        # Create vacant cells divided by walls
        cells = [["║"+("  "*self.scale)] * w + ['║'] for _ in range(h)] + [[]]
        # Create horizontal walls
        wall = [["╬"+("══"*self.scale)] * w + ['╬'] for _ in range(h + 1)]

        # Go around the empty grid to make paths and walls for the maze
        def explore(x:int, y:int) -> None:
            seen[y][x] = 1
            
            # Go over the neighboring cells in the maze and shuffle them
            neighbor = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(neighbor)
           
            for (x1, y1) in neighbor:
                # If the selected cell has been explored, ignore it
                if seen[y1][x1]: 
                    continue
                # Place a wall on the randomly selected side when moving horizontally
                if x1 == x:
                    wall[max(y, y1)][x] = "╬" + ("  "*self.scale)
                # Make a path on the randomly selected side when moving vertically
                if y1 == y:
                    cells[y][max(x, x1)] = " " + ("  "*self.scale)
                explore(x1, y1)

        # Start the exploration on a random position on the empty grid
        explore(randrange(w), randrange(h))
        # Make the ascii form of the maze and store it in self.cells
        def split(word):
            return [char for char in word]
        for (a, b) in zip(wall, cells):
            self.cells.append(split(''.join(a)))
            self.bare.append(split(''.join(a)))
            for n in range(self.scale):
                if len(b) != 0:
                    self.cells.append(split(''.join(b)))
                    self.bare.append(split(''.join(b)))
            print(''.join(a + (['\n'] + b)*self.scale))

    # Make the sequence of line objects to represent the maze, creates rows attribute
    def make_lines(self) -> np.ndarray:
        # Make a copy of the ascii representation of the maze to turn into 1s and 0s
        copy_cells = self.get_cells()
        for ind1, row in enumerate(copy_cells):
            for ind2, cell in enumerate(row):
                if str(cell) == ' ' or str(cell) == 'K':
                    copy_cells[ind1][ind2] = 0
                else:
                    copy_cells[ind1][ind2] = 1
        return copy_cells
        
    # Initialize locations for the player's spawn point and the objective
    def spawn_and_key(self) -> tuple:
        # Get the cells(ascii) and rows(num) of the maze
        wid: int = self.width*(self.scale*2)
        hei: int = self.height*(self.scale)
        cells = self.cells
        rows = self.rows
        # Get the horizontal and vertical range of spaces in the maze 
        hor_range = range(1,wid-2)
        ver_range = range(1,hei-2)
        # Select a random row along the y axis for spawn and key
        y_pos_spawn = randint(1, ver_range[-1])
        # Randomly generate 3 key positions
        y_pos_keys = []
        for n in range(self.num_keys):
            y_pos_keys.append(randint(1, ver_range[-1]))
        # Keep track of whether valid spawn or key positions have been found or not
        key_pos = False
        # Make function that finds a valid position
        def find_pos(a_range: range, y_pos: int):
            # Go over all the cells in the row to find a vacant position
            pos_found = False
            while pos_found == False:
                pos = randint(1, a_range[-1])
                # Exit the while loop if a valid position is found
                if self.cells[y_pos][pos] == ' ':
                    pos_found = True
            return pos
        key_positions = []
        # Make tuples representing the positions of the spawn and key in the maze
        spawn_pos = (y_pos_spawn, find_pos(hor_range, y_pos_spawn))
        # Represent the spawn point with a 3 in the numpy array and a * in the ascii
        self.rows[spawn_pos[0]][spawn_pos[1]] = 2
        # Place the keys in their respective places
        def split(word):
            return [char for char in word]
        empty_keys = []
        for key in y_pos_keys:
            key_pos = (key, find_pos(hor_range, key))
            # Add the positions to the list of key_positions to be returned by the method
            key_positions.append(key_pos)
            self.rows[key_pos[0]][key_pos[1]] = 1
            # Replace the row of cells where the key object is with the edited one with the keys
            key_cells = list(''.join(cells[key]))  
            key_cells[key_pos[1]] = 'K'
            key_cells = ''.join(key_cells)
            #key_cells = [key_cells[i:i+(self.scale*2)] for i in range(0, len(key_cells), (self.scale*2))]
            key_cells = split(key_cells)
            self.cells[key] = key_cells
        # Represent the key and spawn points on the cells attribute
        spawn_cells = list(''.join(cells[y_pos_spawn]))
        spawn_cells[spawn_pos[1]] = '@'
        # Update the row and cells in the maze
        spawn_cells = ''.join(spawn_cells)
        #spawn_cells = [spawn_cells[i:i+(self.scale*2)] for i in range(0, len(spawn_cells), (self.scale*2))]
        spawn_cells = split(spawn_cells)
        self.cells[y_pos_spawn] = spawn_cells
        return (spawn_pos, key_positions)
        
    # Returns the cells of the maze in np form
    def get_cells(self) -> np.ndarray:
        return np.array([np.array(i) for i in self.cells], dtype = object)
        
    # Display the maze
    def display(self, array: np.ndarray) -> None:
        empty = []
        # Join the sequence of characters into one list
        for row in array:
            new_row = ''.join(row)
            empty.append(new_row)
        print('\n'.join(empty))

    def update(self) -> None:
        '''
        Updates the position of the player on screen 
        and checks whether keys have been collected or not
        '''
        bare_copy = self.bare
        player_pos = list(self.player_pos)
        # Look for the player's position in the maze
        for ind1, row in enumerate(self.bare):
            for ind2, cell in enumerate(row):
                for key in self.key_pos:
                    if list(key) == [ind1, ind2]:
                        # If the player and a key are in the same position,
                        # erase the key and put the player in the position
                        if list(key) == player_pos:
                            self.keys_collected += 1
                            self.key_pos.remove(key)
                            bare_copy[ind1,ind2] = '@'
                        else:
                            bare_copy[ind1,ind2] = 'K'
                    else:
                        bare_copy[ind1,ind2] = '@'
        self.display(bare_copy)

    def move(self, key: Literal["left", "right", "up", "down"]) -> None:
        """A function which toggles player movement.
        :param key: Key pressed by the user.
        :type plane: Object, imported from grid.py
        :return: Nothing.
        """
        player_pos = list(self.player_pos)
        if key == 'left' and self.check('left'):
            self.update()
            self.player_pos[1] -= 1
        elif key == 'right' and self.check('right'):
            self.update()
            self.player_pos[1] += 1
        elif key == 'up' and self.check('up'):
            self.update()
            self.player_pos[0] -= 1
        elif key == 'down' and self.check('down'):
            self.update()
            self.player_pos[0] += 1

    def get_key_bindings(self) -> KeyBindings:
        """Add different key bindings to control the player/UI
        :return: KeyBindings Object
        """
        kb = KeyBindings()

        # Exit
        @kb.add("c-c")
        @kb.add("c-q")
        def _(event: KeyPressEvent) -> None:
            event.app.exit()

        # Movement
        @kb.add("a")
        @kb.add("left")
        def go_left(event: KeyPressEvent) -> None:
            self.move('left')
            self.update()

        @kb.add("d")
        @kb.add("right")
        def go_right(event: KeyPressEvent) -> None:
            self.move('right')
            self.update()

        @kb.add("w")
        @kb.add("up")
        def go_up(event: KeyPressEvent) -> None:
            self.move('up')
            self.update()

        @kb.add("s")
        @kb.add("down")
        def go_down(event: KeyPressEvent) -> None:
            self.move('down')
            self.update()

if __name__ == "__main__":
    maze = Maze(10,7,5,2)
    
    
        
