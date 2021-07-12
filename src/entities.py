import os

import numpy as np

ASCII_FOLDER = "../assets/ascii"


class Entity:
    """A base class for creating entities from ascii files.

    Defines attributes x, y, width, height, which_screen as well as method render()
    that can be accessed for rendering.
    """

    def __init__(self, ascii_file: str, x: int, y: int, which_screen: int) -> None:
        """Initialises Entity object based on ASCII stored in file.

        :param ascii_file: The filename containing the ascii art in the ascii folder.
        :param x: The x position of the entity.
        :param y: The y position of the entity.
        :param which_screen: An integer noting which screen the entity is on.
        """
        self.x = x
        self.y = y
        self.which_screen = which_screen

        # Processing ascii file
        with open(os.path.join(ASCII_FOLDER, ascii_file), "r", encoding="utf8") as file:
            ascii_lst = file.read().rstrip().splitlines()

        self.height = len(ascii_lst)  # Finding the height of the ascii art
        self.width = max(
            [len(line) for line in ascii_lst]
        )  # Finding the width of the ascii art

        # Padding out the lines in case needed white space isn't in ascii file
        ascii_lst = [line + (self.width - len(line)) * " " for line in ascii_lst]

        # Storing the rendered table
        self.rendered_table = np.array([list(line) for line in ascii_lst])

    def __repr__(self):
        mutated_table = np.c_[self.rendered_table, np.full((self.height, 1), "\n")]
        return "".join(mutated_table.ravel().tolist())

    def render(self) -> np.ndarray:
        """A method that returns the rendered table as a 2D numpy array."""
        return self.rendered_table


class Tree(Entity):
    """A derived Entity class creating a tree object."""

    def __init__(self, x: int, y: int, which_screen: int) -> None:
        """Creates a tree based on the tree ascii file in the ascii folder."""
        ascii_file = "tree.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen)


class Bar(Entity):
    """A derived Entity class creating a bar object."""

    def __init__(self, x: int, y: int, which_screen: int) -> None:
        """Creates a bar based on the bar ascii file in the ascii folder."""
        ascii_file = "bar.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen)


class Fountain(Entity):
    """A derived Entity class creating a fountain object."""

    def __init__(self, x: int, y: int, which_screen: int) -> None:
        """Creates a fountain based on the fountain ascii file in the ascii folder."""
        ascii_file = "fountain.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen)


if __name__ == "__main__":
    items = [Tree(1, 2, 1), Bar(1, 2, 3), Fountain(1, 2, 3)]
    for item in items:
        print(item.render())
