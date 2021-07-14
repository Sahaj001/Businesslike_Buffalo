import time

from entities import Entity, Tree
from grid import Grid
from person import Person


class Screen:
    """Class to manage multiple game screens"""

    def __init__(self, width: int, height: int):
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        self.BOX_PADDING_X = 24
        self.BOX_PADDING_Y = 12
        self.screens = {i: Grid(self.GRID_WIDTH, self.GRID_HEIGHT) for i in range(1, 10)}
        self.current_screen = 5

        # Screen 1
        self.screens[1].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["┌"])
        for screen_x in range(self.GRID_WIDTH-self.BOX_PADDING_X, self.GRID_WIDTH-1):
            self.screens[1].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(self.GRID_HEIGHT-self.BOX_PADDING_Y, self.GRID_HEIGHT-1):
            self.screens[1].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 2
        for screen_x in range(0, self.GRID_WIDTH-1):
            self.screens[2].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])

        # Screen 3
        self.screens[3].insert(self.BOX_PADDING_X - 1, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["┐"])
        for screen_x in range(0, self.BOX_PADDING_X-1):
            self.screens[3].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(self.GRID_HEIGHT-self.BOX_PADDING_Y, self.GRID_HEIGHT-1):
            self.screens[3].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 4
        for screen_y in range(0, self.GRID_HEIGHT-1):
            self.screens[4].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 5
        #  self.screens[5].insert(0, 0, ["┌"])
        #  self.screens[5].insert(0, self.GRID_HEIGHT-1, ["└"])
        #  for screen_x in range(1, self.GRID_WIDTH-1):
        #      self.screens[5].insert(screen_x, 0, ["─"])
        #      self.screens[5].insert(screen_x, self.GRID_HEIGHT-1, ["─"])
        #  self.screens[5].insert(self.GRID_WIDTH-1, 0, ["┐"])
        #  self.screens[5].insert(self.GRID_WIDTH-1, self.GRID_HEIGHT-1, ["┘"])
        #  for screen_y in range(1, self.GRID_HEIGHT-1):
        #      self.screens[5].insert(0, screen_y, ["│"])
        #      self.screens[5].insert(self.GRID_WIDTH-1, screen_y, ["│"])

        # Screen 6
        for screen_y in range(0, self.GRID_HEIGHT-1):
            self.screens[6].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 7
        self.screens[7].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, self.BOX_PADDING_Y-1, ["└"])
        for screen_x in range(self.GRID_WIDTH-self.BOX_PADDING_X, self.GRID_WIDTH-1):
            self.screens[7].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(0, self.BOX_PADDING_Y-1):
            self.screens[7].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 8
        for screen_x in range(0, self.GRID_WIDTH-1):
            self.screens[8].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])

        # Screen 9
        self.screens[9].insert(self.BOX_PADDING_X-1, self.BOX_PADDING_Y-1, ["┘"])
        for screen_x in range(0, self.BOX_PADDING_X-1):
            self.screens[9].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(0, self.BOX_PADDING_Y-1):
            self.screens[9].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

    def insert_entity(self, entity: Entity, ignore_presence: bool = False) -> None:
        """Inserts a object of entity class to its specified point in the current screen.

        :param ignore_presence: Doesn't changes the binary matrix if it is False.
        :type entity: Object, imported from entities.py
        """
        self.screens[self.current_screen].add_entity(entity, ignore_presence)

    def update_entity(self, entity: Entity, ignore_presence: bool = False) -> None:
        """Updates an entity object's position

        :type entity: Object, imported from entities.py
        :param ignore_presence: Doesn't changes the binary matrix if it is False refer to grid->Grid->insert_entity.
        :return:
        """
        if entity.x >= self.GRID_WIDTH:
            self.screens[self.current_screen].remove_entity(entity.unique_name)
            self.current_screen += 1
            self.screens[self.current_screen].add_entity(entity, ignore_presence)
            entity.set_coordinates(0, entity.y)
        elif entity.x < 0:
            self.screens[self.current_screen].remove_entity(entity.unique_name)
            self.current_screen -= 1
            self.screens[self.current_screen].add_entity(entity, ignore_presence)
            entity.set_coordinates(self.GRID_WIDTH-1, entity.y)
        if entity.y < 0:
            self.screens[self.current_screen].remove_entity(entity.unique_name)
            self.current_screen -= 3
            self.screens[self.current_screen].add_entity(entity, ignore_presence)
            entity.set_coordinates(entity.x, self.GRID_HEIGHT-2)
        if entity.y >= self.GRID_HEIGHT-1:
            self.screens[self.current_screen].remove_entity(entity.unique_name)
            self.current_screen += 3
            self.screens[self.current_screen].add_entity(entity, ignore_presence)
            entity.set_coordinates(entity.x, 0)

    def get_current_screen(self) -> Grid:
        """Get the Grid object for the current screen

        :returns: Grid Object of current screen
        """
        return self.screens[self.current_screen]

    def render(self) -> str:
        """Get the string format of the grid

        :returns: string format of the grid for the current screen
        """
        self.screens[self.current_screen].render_screen()
        return str(self.screens[self.current_screen])
