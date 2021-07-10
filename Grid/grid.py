import numpy as np


class Grid:
    """Used to create grid in which objects can be rendered.

    If you ever see the word point in this file it means the cartesian point i.e (x,y).
    """

    def __init__(self, width: int = 100, height: int = 100):
        """Initialises the arguments.

        :param width: The width of the grid
        :param height: The height of the grid
        """
        self.width = width - 1
        self.height = height - 1
        grid = np.full((height, width), " ")
        self.grid = grid

    def __repr__(self) -> str:
        self.grid = np.c_[self.grid, np.full((self.height+1, 1), "\n")]
        return ''.join(self.grid.ravel())

    def insert(self, pos_x: int, pos_y: int, object_to_be_rendered: list, object_height: int = 1,
               object_width: int = 1) -> None:
        """Inserts a object to the specified point.

        :param pos_x: The x axis point of the grid where object is to be rendered.
        :param pos_y: The y axis point of the grid where object is to be rendered.
        :param object_to_be_rendered: The object you want to render.
        :param object_width: The object's width.
        :param object_height: The object's height.
        :return: Nothing.
        """
        self.grid[pos_y:pos_y + object_height, pos_x:pos_x+object_width] = np.array(object_to_be_rendered)

    def check(self, pos_x: int, pos_y: int) -> bool:
        """Checks whether the user specified point is blank or not

        :param pos_x: The x axis point of the grid where the user want to check.
        :param pos_y: The y axis point of the grid where the user want to check.
        :return: A boolean object.
        """
        user_point = self.grid[pos_y:pos_y + 1, pos_x:pos_x + 1]
        if user_point == " ":
            # Checks if the point is empty, if yes it returns True if no then it returns False.
            return True
        else:
            return False


if __name__ == "__main__":
    plane = Grid(80, 24)
    plane.insert(0, 0, ["┌"])
    plane.insert(0, 23, ["└"])
    for plane_x in range(1, 79):
        plane.insert(plane_x, 0, ["─"])
        plane.insert(plane_x, 23, ["─"])
    plane.insert(79, 0, ["┐"])
    plane.insert(79, 23, ["┘"])

    for plane_y in range(1, 23):
        plane.insert(0, plane_y, ["│"])
        plane.insert(79, plane_y, ["│"])
    plane.insert(1, 1, ["w", 'w', 'w', 'w', 'w', 'w', 'w', 'w'], object_width=8)
    print(plane)
