import time

from entities import Entity
from grid import Grid
from person import Person


class Screen:
    """Class to manage multiple game screens"""

    def __init__(self, width: int, height: int):
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        self.BOX_PADDING_X = 24
        self.BOX_PADDING_Y = 12
        self.screens = []
        for i in range(9):
            self.screens.append(Grid(self.GRID_WIDTH, self.GRID_HEIGHT))
        self.current_screen = 5

        # Screen 1 (index 0)
        self.screens[0].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["┌"])
        for screen_x in range(self.GRID_WIDTH-self.BOX_PADDING_X, self.GRID_WIDTH-1):
            self.screens[0].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(self.GRID_HEIGHT-self.BOX_PADDING_Y, self.GRID_HEIGHT-1):
            self.screens[0].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 2 (index 1)
        for screen_x in range(0, self.GRID_WIDTH-1):
            self.screens[1].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])

        # Screen 3 (index 2)
        self.screens[2].insert(self.BOX_PADDING_X - 1, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["┐"])
        for screen_x in range(0, self.BOX_PADDING_X-1):
            self.screens[2].insert(screen_x, self.GRID_HEIGHT-self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(self.GRID_HEIGHT-self.BOX_PADDING_Y, self.GRID_HEIGHT-1):
            self.screens[2].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 4 (index 3)
        for screen_y in range(0, self.GRID_HEIGHT-1):
            self.screens[3].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 5 (index 4)
        #  self.screens[4].insert(0, 0, ["┌"])
        #  self.screens[4].insert(0, self.GRID_HEIGHT-1, ["└"])
        #  for screen_x in range(1, self.GRID_WIDTH-1):
        #      self.screens[4].insert(screen_x, 0, ["─"])
        #      self.screens[4].insert(screen_x, self.GRID_HEIGHT-1, ["─"])
        #  self.screens[4].insert(self.GRID_WIDTH-1, 0, ["┐"])
        #  self.screens[4].insert(self.GRID_WIDTH-1, self.GRID_HEIGHT-1, ["┘"])
        #  for screen_y in range(1, self.GRID_HEIGHT-1):
        #      self.screens[4].insert(0, screen_y, ["│"])
        #      self.screens[4].insert(self.GRID_WIDTH-1, screen_y, ["│"])

        # Screen 6 (index 5)
        for screen_y in range(0, self.GRID_HEIGHT-1):
            self.screens[5].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 7 (index 6)
        self.screens[6].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, self.BOX_PADDING_Y-1, ["└"])
        for screen_x in range(self.GRID_WIDTH-self.BOX_PADDING_X, self.GRID_WIDTH-1):
            self.screens[6].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(0, self.BOX_PADDING_Y-1):
            self.screens[6].insert(self.GRID_WIDTH-self.BOX_PADDING_X-1, screen_y, ["│"])

        # Screen 8 (index 7)
        for screen_x in range(0, self.GRID_WIDTH-1):
            self.screens[7].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])

        # Screen 9 (index 8)
        self.screens[8].insert(self.BOX_PADDING_X-1, self.BOX_PADDING_Y-1, ["┘"])
        for screen_x in range(0, self.BOX_PADDING_X-1):
            self.screens[8].insert(screen_x, self.BOX_PADDING_Y-1, ["─"])
        for screen_y in range(0, self.BOX_PADDING_Y-1):
            self.screens[8].insert(self.BOX_PADDING_X-1, screen_y, ["│"])

    def insertEntity(self, entity: Entity) -> None:
        """Inserts a object of entity class to its specified point in the current screen.

        :param person: Object, imported from entities.py
        """
        self.screens[self.current_screen - 1].insert_entity(entity)

    def updateEntity(self, entity: Entity) -> None:
        """Updates an entity object's position

        :param person: Object, imported from entity.py
        :return:
        """
        # To be fixed
        if entity.x >= self.GRID_WIDTH:
            self.current_screen += 1
        if entity.x < 0:
            self.current_screen -= 1

        self.screens[self.current_screen - 1].update_entity(entity, p.old_x, p.old_y)

    def getCurrentScreen(self) -> Grid:
        """Get the Grid object for the current screen

        :returns: Gridd Object of current screen
        """
        return self.screens[self.current_screen - 1]

    def render(self) -> str:
        """Get the stringified grid

        :returns: stringified grid of current screen
        """
        return str(self.screens[self.current_screen - 1])


# For testing
if __name__ == '__main__':
    screen = Screen(88, 24)
    p = Person(5, 5, 1)
    screen.insertEntity(p)
    for i in range(10):
        p.move('left', screen.getCurrentScreen())
        screen.updateEntity(p)
        print(screen.render())
        time.sleep(1)
