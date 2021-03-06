from typing import Literal

import entities
import grid


class Person(entities.Entity):
    """The Person class or the player is a controllable Entity in the game."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str):
        """Creates a person based on the person ascii file in the ascii folder."""
        ascii_file = "person.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)
        self.facing = 'left'
        self.old_x = x
        self.old_y = y

    def adjust_face(self, direction: str) -> None:
        """Adjusts the face based on the current direction the user moved.

        :return: Nothing.
        """
        direction_dict = {'left': 'И', 'right': 'N'}
        self.rendered_table[1:2] = [direction_dict[direction]]

    def move(self, key: Literal["left", "right", "up", "down"], plane: grid.Grid) -> None:
        """A function which toggles player movement.

        :param key: Key pressed by the user.
        :type plane: Object, imported from grid.py
        :return: Nothing.
        """
        if key == 'left' and plane.check(self, 'left'):
            self.update()
            if self.facing != key:
                self.facing = key
                self.adjust_face(key)
            self.x -= 1
        elif key == 'right' and plane.check(self, 'right'):
            self.update()
            if self.facing != key:
                self.facing = key
                self.adjust_face(key)
            self.x += 1
        elif key == 'up' and plane.check(self, 'up'):
            self.update()
            self.y -= 1
        elif key == 'down' and plane.check(self, 'down'):
            self.update()
            self.y += 1

    def update(self) -> None:
        """Updates old co-ordinates of the person/player.

        :return: Nothing
        """
        self.old_y = self.y
        self.old_x = self.x
