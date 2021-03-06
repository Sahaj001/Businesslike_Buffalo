import typing
from typing import List, Union

import numpy as np

import entities


class Grid:
    """Used to create grid in which objects can be rendered.

    If you ever see the word point in this file it means the cartesian point i.e (x,y).
    """

    def __init__(self, width: int = 80, height: int = 24):
        """Initializes the arguments.

        :param width: The width of the grid
        :param height: The height of the grid
        """
        self.width = width - 1
        self.height = height - 1
        self.initialize_grid()
        self.grid_bin = np.zeros((height, width))
        self.grid_entities = []

    def __repr__(self) -> str:
        # Replacing null bytes with whitespace
        grid = self.grid
        grid[grid == "\u2800"] = " "
        mutated_grid = np.c_[grid, np.full((self.height + 1, 1), "\n")]
        return "".join(mutated_grid.ravel())

    def add_entity(self, entity: entities.Entity, presence: bool = False) -> None:
        """Adds a specified entity to the grid."""
        self.grid_entities.append((entity, presence))
        return

    def initialize_grid(self) -> None:
        """Initializes the grid to be an array of space characters."""
        grid = np.full((self.height+1, self.width+1), " ")
        self.grid = grid
        return

    def remove_entity(self, entity_unique_name: str) -> None:
        """Given the unique entity name, it will remove the entity from the grid."""
        names = [entity[0].unique_name for entity in self.grid_entities]
        try:
            name_index = names.index(entity_unique_name)
        except ValueError:
            raise Exception(f"No entity of name '{entity_unique_name}' on screen.")

        # Removing the specified entity
        self.grid_entities.pop(name_index)
        return

    def render_screen(self) -> str:
        """Renders all entities in self.grid_entities into the grid.

        It renders those of lower y value before those of greater y value.
        """
        sorted_entities = sorted(self.grid_entities, key=lambda entity_: entity_[0].x)
        self.initialize_grid()

        for entity, presence in sorted_entities:
            self.insert_entity(entity, presence)
        return str(self)

    def insert(
            self,
            pos_x: int,
            pos_y: int,
            object_to_be_rendered: Union[List[str], List[List]],
            object_height: int = 1,
            object_width: int = 1,
    ) -> None:
        """Inserts a object to the specified point.

        :param pos_x: The x axis point of the grid where object is to be rendered.
        :param pos_y: The y axis point of the grid where object is to be rendered.
        :param object_to_be_rendered: The object you want to render.
        :param object_width: The object's width.
        :param object_height: The object's height.
        :return: Nothing.
        """
        self.grid[pos_y:pos_y + object_height, pos_x:pos_x + object_width] = np.array(object_to_be_rendered)

    def check(self, entity: entities.Entity, direction: typing.Literal["left", "up", "down", "right"]) -> bool:
        """Checks whether the user specified point is blank or not

        :type entity: object, imported from entities.py
        :param direction : The direction in which you want to check
        :return: A boolean object.
        """
        if direction == "left":
            user_point = self.grid_bin[entity.y:entity.y + entity.height, entity.x - 1:entity.x]

        elif direction == "right":
            user_point = self.grid_bin[entity.y:entity.y + entity.height,
                                       entity.x + entity.width:entity.x + entity.width + 1]
        elif direction == "up":
            user_point = self.grid_bin[entity.y - 1:entity.y, entity.x:entity.x + entity.width]

        else:
            # also could be written as elif direction == "down".
            user_point = self.grid_bin[entity.y + entity.height:entity.y + entity.height + 1,
                                       entity.x:entity.x + entity.width]

        if np.all(user_point == 0):
            # Checks if the point is empty, if yes it returns True if no then it returns False.
            return True
        else:
            return False

    def insert_entity(self, entity: entities.Entity, ignore_presence: bool = False) -> None:
        """Inserts a object of entity class to its specified point.

        :type entity: Object, imported from entities.py
        :param ignore_presence: Doesn't changes the binary matrix if it is False.
        """
        ascii_render = entity.render()
        self.grid[entity.y: entity.y + entity.height, entity.x: entity.x + entity.width] = ascii_render

        if not ignore_presence:
            # Checks where the non-whitespace characters are, and creates an array of 1s in their locations
            boolean_array = (ascii_render != " ").astype(int)
            self.grid_bin[entity.y: entity.y + entity.height, entity.x: entity.x + entity.width] = boolean_array
