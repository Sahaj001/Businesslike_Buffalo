import os
import numpy as np

ASCII_FOLDER = "assets/ascii"


class Entity:
    def __init__(self, ascii_file: str, x: int, y: int, which_screen: int) -> None:
        """Initialises Entity object based on ASCII stored in file"""
        self.x = x
        self.y = y
        self.which_screen = which_screen

        # Processing ascii file
        with open(os.path.join(ASCII_FOLDER, ascii_file), "r", encoding="utf8") as file:
            ascii_lst = file.read().strip().splitlines()

        self.height = len(ascii_lst)  # Finding the height of the ascii art
        self.width = max([len(line) for line in ascii_lst])  # Finding the width of the ascii art

        # Padding out the lines in case needed white space isn't in ascii file
        ascii_lst = [line + (self.width-len(line))*" " for line in ascii_lst]

        # Storing the rendered table
        self.rendered_table = np.array([list(line) for line in ascii_lst])

    def render(self) -> np.ndarray:
        """A method that returns the rendered table"""
        return self.rendered_table


class Tree(Entity):
    def __init__(self, x: int, y: int, which_screen: int):
        ascii_file = "tree.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen)


class Bar(Entity):
    def __init__(self, x: int, y: int, which_screen: int):
        ascii_file = "bar.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen)
