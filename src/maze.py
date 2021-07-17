import typing
from random import randint, randrange, shuffle
from typing import Literal

import numpy as np
from numpy.lib.polynomial import polyval
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout.containers import (
    Float, FloatContainer, HSplit, Window, WindowAlign
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea
import play_sound
import time
import playsound

class Maze:
    '''
    A class that randomly generates a maze with a set width and height.
    It can be represented in text(cells) and numpy array form(rows)
    '''

    # Initialize values of the maze object
    def __init__(self, width: int, height: int, num_keys: int, scale: int = 1) -> None:
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
        self.game_field = TextArea(text=self.display(self.cells))

        self.message_box = TextArea(text="You have collected " + str(self.keys_collected)+"/" + str(self.num_keys) + " keys")

        self.container = HSplit(
            [
                self.game_field,
                Window(height=1, char="-", style="class:line"),
                self.message_box
            ]
        )

        self.body = FloatContainer(
            content=self.container,
            floats=[
                Float(
                    Frame(
                        Window(FormattedTextControl("Maze"), width=22, height=1),
                    ),
                    right=5,
                    top=2,
                )
            ]
        )

        self.kb = KeyBindings()

        # Exit
        @self.kb.add("q")
        @self.kb.add("c-c")
        def _(event: KeyPressEvent) -> None:
            time.sleep(1)
            event.app.exit()

        # Movement
        @self.kb.add("left")
        def go_left(event: KeyPressEvent) -> None:
            self.move('left')
            new_text = self.display(self.cells)
            self.game_field.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            new_text = "You have collected " + str(self.keys_collected)+ "/" + str(self.num_keys) + " keys"
            self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            if self.num_keys == self.keys_collected:
                new_text = "You have completed the maze, well done!"
                self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
                event.app.exit()

        @self.kb.add("right")
        def go_right(event: KeyPressEvent) -> None:
            self.move('right')
            new_text = self.display(self.cells)
            self.game_field.buffer.document = Document(text=new_text)
            new_text = "You have collected " + str(self.keys_collected)+ "/" + str(self.num_keys) + " keys"
            self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            if self.num_keys == self.keys_collected:
                new_text = "You have completed the maze, well done!"
                self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
                event.app.exit()

        @self.kb.add("up")
        def go_up(event: KeyPressEvent) -> None:
            self.move('up')
            new_text = self.display(self.cells)
            self.game_field.buffer.document = Document(text=new_text)
            new_text = "You have collected " + str(self.keys_collected)+ "/" + str(self.num_keys) + " keys"
            self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            if self.num_keys == self.keys_collected:
                new_text = "You have completed the maze, well done!"
                self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
                event.app.exit()

        @self.kb.add("down")
        def go_down(event: KeyPressEvent) -> None:
            self.move('down')
            new_text = self.display(self.cells)
            self.game_field.buffer.document = Document(text=new_text)
            new_text = "You have collected " + str(self.keys_collected)+ "/" + str(self.num_keys) + " keys"
            self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            if self.num_keys == self.keys_collected:
                new_text = "You have completed the maze, well done!"
                self.message_box.buffer.document = Document(text=new_text, cursor_position=len(new_text))
                event.app.exit()

        self.application = Application(
            layout=Layout(self.body),
            key_bindings=self.kb,
            mouse_support=True,
            full_screen=True,
            refresh_interval=0.5
        )

    def sfx(self, object: str):

        if object == " ":
            # play walk.mp3
            playsound.playsound('../boxedin_walksofter.mp3', False)
            # audio.play()
        elif object == "K":
            # play key.mp3
            playsound.playsound('../boxedin_collect.mp3', False)
            # audio.play()
        elif object == "O":
            # play game_over.mp3
            playsound.playsound('../boxedin_levelcomplete.mp3', False)
            # audio.play()
        elif object == "W":
            # play wall.mp3
            playsound.playsound('../boxedin_wall.mp3', False)
            # audio.play()

    def check(self, direction: typing.Literal["left", "up", "down", "right"]) -> bool:
        """Checks whether the user specified point is blank or not
        :type entity: object, imported from entities.py
        :param direction : The direction in which you want to check
        :return: A boolean object.
        """
        player_pos = self.player_pos
        if direction == "left":
            user_point = self.rows[
                player_pos[0]:player_pos[0] + 1, player_pos[1] - 1:player_pos[1]]

        elif direction == "right":
            user_point = self.rows[player_pos[0]:player_pos[0] + 1,
                                   player_pos[1] + 1:player_pos[1] + 1 + 1]

        elif direction == "up":
            user_point = self.rows[
                player_pos[0] - 1:player_pos[0], player_pos[1]:player_pos[1] + 1]
        else:
            # also could be written as elif direction == "down".
            user_point = self.rows[player_pos[0]+1:player_pos[0] + 1 + 1,
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
        def explore(x: int, y: int) -> None:
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
                if str(cell) == ' ' or str(cell) == 'K' or str(cell) == '@':
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
        # rows = self.rows
        # Get the horizontal and vertical range of spaces in the maze
        hor_range = range(1, wid-2)
        ver_range = range(1, hei-2)
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
            while pos_found is False:
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

        for key in y_pos_keys:
            key_pos = (key, find_pos(hor_range, key))
            # Add the positions to the list of key_positions to be returned by the method
            key_positions.append(key_pos)
            self.rows[key_pos[0]][key_pos[1]] = 1
            # Replace the row of cells where the key object is with the edited one with the keys
            key_cells = list(''.join(cells[key]))
            key_cells[key_pos[1]] = 'K'
            key_cells = ''.join(key_cells)
            # key_cells = [key_cells[i:i+(self.scale*2)] for i in range(0, len(key_cells), (self.scale*2))]
            key_cells = split(key_cells)
            self.cells[key] = key_cells
        # Represent the key and spawn points on the cells attribute
        spawn_cells = list(''.join(cells[y_pos_spawn]))
        spawn_cells[spawn_pos[1]] = '@'
        # Update the row and cells in the maze
        spawn_cells = ''.join(spawn_cells)
        # spawn_cells = [spawn_cells[i:i+(self.scale*2)] for i in range(0, len(spawn_cells), (self.scale*2))]
        spawn_cells = split(spawn_cells)
        self.cells[y_pos_spawn] = spawn_cells
        return (spawn_pos, key_positions)

    # Returns the cells of the maze in np form
    def get_cells(self) -> np.ndarray:
        return np.array([np.array(i) for i in self.cells], dtype=object)

    # Display the maze
    def display(self, array: np.ndarray) -> str:
        empty = []
        # Join the sequence of characters into one list
        for row in array:
            new_row = ''.join(row)
            empty.append(new_row)
        return str('\n'.join(empty))

    # Update the maze after every move
    def update(self, old_pos, player_pos) -> None:
        cells = self.cells
        new_pos = cells[player_pos[0]][player_pos[1]]
        if new_pos == ' ':
            self.sfx(object=new_pos)
            self.cells[player_pos[0]][player_pos[1]] = '@'
            self.cells[old_pos[0]][old_pos[1]] = ' '
        elif new_pos == 'K':
            self.sfx(object="K")
            self.cells[player_pos[0]][player_pos[1]] = '@'
            self.cells[old_pos[0]][old_pos[1]] = ' '
            self.keys_collected += 1
        else:
            self.sfx(object="W")

        if self.keys_collected == self.num_keys:
            self.sfx(object="O")

        '''
        Updates the position of the player on screen
        and checks whether keys have been collected or not
        bare_copy = self.bare
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
                            bare_copy[ind1][ind2] = '@'
                        else:
                            bare_copy[ind1][ind2] = 'K'
                    else:
                        bare_copy[ind1][ind2] = '@'
        self.display(bare_copy)
        '''

    def move(self, key: Literal["left", "right", "up", "down"]) -> None:
        """A function which toggles player movement.
        :param key: Key pressed by the user.
        :type plane: Object, imported from grid.py
        :return: Nothing.
        """
        player_pos = list(self.player_pos)
        old_pos = list(self.player_pos)
        if key == 'left' and self.check('left'):
            player_pos[1] -= 1
            self.player_pos = player_pos
            self.update(old_pos, player_pos)
        elif key == 'right' and self.check('right'):
            player_pos[1] += 1
            self.player_pos = player_pos
            self.update(old_pos, player_pos)
        elif key == 'up' and self.check('up'):
            player_pos[0] -= 1
            self.player_pos = player_pos
            self.update(old_pos, player_pos)
        elif key == 'down' and self.check('down'):
            player_pos[0] += 1
            self.player_pos = player_pos
            self.update(old_pos, player_pos)


if __name__ == "__main__":
    maze = Maze(13, 5, 5, scale=3)
    maze.application.run()
