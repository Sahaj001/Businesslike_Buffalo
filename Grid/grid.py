def create_line(width_of_line: int) -> str:
    """Returns a line.

    :param width_of_line: The width of the line it wants to create.
    :return: A string having length width_of_line
    """
    line = ""
    for _ in range(width_of_line):
        line += " "
    return line


class Grid:
    """
    Used to create grid in which objects can be rendered.
    If you ever see the word point in this file it means the cartesian point i.e (x,y).
    """

    def __init__(self, width: int = 100, height: int = 100):
        """Initialises the arguments.

        :param width: The width of the grid
        :param height: The height of the grid
        """
        self.width = width
        self.height = height
        grid = []
        for _ in range(height):
            line = create_line(width_of_line=width)
            grid.append(line)
        self.grid = grid

    def __repr__(self) -> str:
        return '\n'.join(self.grid)

    def insert(self, pos_x: int, pos_y: int, object_to_be_rendered: str) -> None:
        """Inserts a object to the specified point.

        :param pos_x: The x axis point of the grid where object is to be rendered.
        :param pos_y: The y axis point of the grid where object is to be rendered.
        :param object_to_be_rendered: The object you want to render.
        :return: Nothing.
        """
        line = self.grid[pos_y]
        # Converts line to a list.
        mutated_line = list(map(lambda line_elem: line_elem, line))
        # Adds the object to the desired place.
        mutated_line[pos_x] = object_to_be_rendered
        # Converts the line to a string.
        self.grid[pos_y] = ''.join(mutated_line)

    def check(self, pos_x: int, pos_y: int) -> bool:
        """Checks whether the user specified point is blank or not

        :param pos_x: The x axis point of the grid where the user want to check.
        :param pos_y: The y axis point of the grid where the user want to check.
        :return: A boolean object.
        """
        line = self.grid[pos_y]
        # Converts line to a list.
        mutated_line = list(map(lambda line_elem: line_elem, line))
        # Gets the point where the user want to check.
        user_point = mutated_line[pos_x]

        if user_point == " ":
            # Checks if the point is empty, if yes it returns True if no then it returns False.
            return True
        else:
            return False


if __name__ == "__main__":
    plane = Grid()
    plane.insert(0, 0, "┌")
    plane.insert(0, 99, "└")
    for plane_x in range(1, 99):
        plane.insert(plane_x, 0, "─")
        plane.insert(plane_x, 99, "─")
    plane.insert(99, 0, "┐")
    plane.insert(99, 99, "┘")

    for plane_y in range(1, 99):
        plane.insert(0, plane_y, "│")
        plane.insert(99, plane_y, "│")

    print(plane)
