import typing
from typing import List, Union

import numpy as np
import entities
import person


class Grid:
    """Used to create grid in which objects can be rendered.

    If you ever see the word point in this file it means the cartesian point i.e (x,y).
    """

    def __init__(self, width: int = 80, height: int = 24):
        """Initialises the arguments.

        :param width: The width of the grid
        :param height: The height of the grid
        """
        self.width = width - 1
        self.height = height - 1
        grid = np.full((height, width), " ")
        self.grid = grid

    def __repr__(self) -> str:
        mutated_grid = np.c_[self.grid, np.full((self.height + 1, 1), "\n")]
        return ''.join(mutated_grid.ravel())

    def insert(self, pos_x: int, pos_y: int, object_to_be_rendered: Union[List[str], List[List]],
               object_height: int = 1,
               object_width: int = 1) -> None:
        """Inserts a object to the specified point.

        :param pos_x: The x axis point of the grid where object is to be rendered.
        :param pos_y: The y axis point of the grid where object is to be rendered.
        :param object_to_be_rendered: The object you want to render.
        :param object_width: The object's width.
        :param object_height: The object's height.
        :return: Nothing.
        """
        self.grid[pos_y:pos_y + object_height, pos_x:pos_x + object_width] = np.array(object_to_be_rendered)

    def check(self, entity: entities.Entity, direction: typing.Literal['left', 'up', 'down', 'right']) -> bool:
        """Checks whether the user specified point is blank or not

        :type entity: object, imported from entities.py
        :param direction : The direction in which you want to check
        :return: A boolean object.
        """
        if direction == "left":
            user_point = self.grid[entity.y:entity.y+entity.height, entity.x-1:entity.x]
        elif direction == "right":
            user_point = self.grid[entity.y:entity.y+entity.height, entity.x+entity.width:entity.x + 2]
        elif direction == "up":
            user_point = self.grid[entity.y-1:entity.y, entity.x:entity.x+entity.width]
        else:
            # also could be written as elif direction == "down".
            user_point = self.grid[entity.y+entity.height: entity.y+2, entity.x:entity.x+entity.width]

        print(user_point)

        if np.all(user_point == " "):
            # Checks if the point is empty, if yes it returns True if no then it returns False.
            return True
        else:
            return False

    def insert_entity(self, entity: entities.Entity) -> None:
        """Inserts a object of entity class to its specified point.

        :type entity: Object, imported from entities.py
        """
        self.grid[entity.y: entity.y + entity.height, entity.x: entity.x + entity.width] = entity.render()

    def update_entity(self, entity: entities.Entity, old_x: int, old_y: int) -> None:
        """Updates an entity object's position

        :param old_x: The old x axis point of the object before it moved.
        :param old_y: The old y axis point of the object before it moved.
        :type entity: Object, imported from entity.py
        :return:
        """
        self.grid[old_y:old_y + entity.height, old_x:old_x + entity.width] = \
            np.full((np.size(entity.render(), 0), np.size(entity.render(), 1)), " ")

        self.grid[entity.y:entity.y + entity.height, entity.x:entity.width + entity.x] = entity.render()


if __name__ == "__main__":
    p = person.Person(5, 5, 1)
    plane1 = Grid(12, 12)
    plane1.insert_entity(p)
    plane1.insert(0, 0, ["┌"])
    plane1.insert(0, 11, ["└"])
    for plane1_x in range(1, 11):
        plane1.insert(plane1_x, 0, ["─"])
        plane1.insert(plane1_x, 11, ["─"])
    plane1.insert(11, 0, ["┐"])
    plane1.insert(11, 11, ["┘"])

    for plane1_y in range(1, 11):
        plane1.insert(0, plane1_y, ["│"])
        plane1.insert(11, plane1_y, ["│"])

    # while True:
    #     os.system('clear')
    #     user_response = random.choice(['right'])
    #     print(user_response)
    #     p.move(user_response, plane1)
    #     plane1.update_entity(p, p.old_x, p.old_y)
    #     print(plane1)
    #     time.sleep(1)
