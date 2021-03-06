import os

import numpy as np

ASCII_FOLDER = "../assets/ascii"


class Entity:
    """A base class for creating entities from ascii files.

    Defines attributes x, y, width, height, which_screen as well as method render()
    that can be accessed for rendering.
    """

    def __init__(
            self, ascii_file: str, x: int, y: int, which_screen: int, unique_name: str
    ) -> None:
        """Initializes Entity object based on ASCII stored in file.

        :param ascii_file: The filename containing the ascii art in the ascii folder.
        :param x: The x position of the entity.
        :param y: The y position of the entity.
        :param which_screen: An integer noting which screen the entity is on.
        """
        self.x = x
        self.y = y
        self.which_screen = which_screen
        self.unique_name = unique_name

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

    def set_coordinates(self, x: int, y: int) -> None:
        """Set the player coordinates

        :param x: X coordinates to set
        :param y: Y coordinates to set
        """
        self.x = x
        self.y = y

    def __repr__(self):
        mutated_table = np.c_[self.rendered_table, np.full((self.height, 1), "\n")]
        return "".join(mutated_table.ravel().tolist())

    def render(self) -> np.ndarray:
        """A method that returns the rendered table as a 2D numpy array."""
        return self.rendered_table


class Wall(Entity):
    """A derived Entity class creating a wall object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a tree based on the tree ascii file in the ascii folder."""
        ascii_file = "wall.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Tree(Entity):
    """A derived Entity class creating a tree object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a tree based on the tree ascii file in the ascii folder."""
        ascii_file = "tree.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class WitchHut(Entity):
    """A derived Entity class creating a which hut object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a which hut based on the which hut ascii file in the ascii folder."""
        ascii_file = "witch_hut.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class House(Entity):
    """A derived Entity class creating a house object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a house based on the house ascii file in the ascii folder."""
        ascii_file = "house.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Bar(Entity):
    """A derived Entity class creating a bar object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a bar based on the bar ascii file in the ascii folder."""
        ascii_file = "bar.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Fountain(Entity):
    """A derived Entity class creating a fountain object."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates a fountain based on the fountain ascii file in the ascii folder."""
        ascii_file = "fountain.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Lake(Entity):
    """A derived Entity class."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates an entity based on the ascii file in the ascii folder."""
        ascii_file = "lake.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class CampFire(Entity):
    """A derived Entity class."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates an entity based on the ascii file in the ascii folder."""
        ascii_file = "campfire.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Tent(Entity):
    """A derived Entity class."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Creates an entity based on the ascii file in the ascii folder."""
        ascii_file = "tent.txt"
        super().__init__(ascii_file=ascii_file, x=x, y=y, which_screen=which_screen, unique_name=unique_name)


class Grass:
    """Define grass."""

    def __init__(self, x: int, y: int, which_screen: int, unique_name: str) -> None:
        """Initialize Grass object based on internal probability.

        :param x: The x position of the entity.
        :param y: The y position of the entity.
        :param which_screen: An integer noting which screen the entity is on.
        """
        self.x = x
        self.y = y
        self.which_screen = which_screen
        self.unique_name = unique_name

        self.height = 4
        self.width = 10
        threshold = 0.6  # Probability of a comma (grass character)

        table = np.full((self.height, self.width), " ")
        grass_bool_mask = (np.random.rand(*table.shape) <= threshold)
        table[grass_bool_mask] = ","

        # Storing the rendered table
        self.rendered_table = table

    def set_coordinates(self, x: int, y: int) -> None:
        """Set the player coordinates

        :param x: X coordinates to set
        :param y: Y coordinates to set
        """
        self.x = x
        self.y = y

    def render(self) -> np.ndarray:
        """Render the Grass"""
        return self.rendered_table
