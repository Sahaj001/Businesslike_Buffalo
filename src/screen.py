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

    def insertEntity(self, entity: Entity) -> None:
        """Inserts a object of entity class to its specified point in the current screen.

        :param person: Object, imported from entities.py
        """
        self.screens[self.current_screen].add_entity(entity)

    def updateEntity(self, entity: Entity) -> None:
        """Updates an entity object's position

        :param person: Object, imported from entity.py
        :return:
        """
        if entity.x >= self.GRID_WIDTH:
            self.current_screen += 1
            entity.setCoords(0, entity.y)
        elif entity.x < 0:
            self.current_screen -= 1
            entity.setCoords(self.GRID_WIDTH-1, entity.y)
        # To be fixed
        if entity.y < 0:
            self.current_screen -= 3
            entity.setCoords(entity.x, self.GRID_HEIGHT-1)
        if entity.y >= self.GRID_HEIGHT:
            self.current_screen += 3
            entity.setCoords(entity.x, 0)

        # self.screens[self.current_screen].update_entity(entity, p.old_x, p.old_y)

    def getCurrentScreen(self) -> Grid:
        """Get the Grid object for the current screen

        :returns: Grid Object of current screen
        """
        return self.screens[self.current_screen]

    def render(self) -> str:
        """Get the stringified grid

        :returns: stringified grid of current screen
        """
        return str(self.screens[self.current_screen])


# For testing
if __name__ == '__main__':
    screen = Screen(88, 24)
    p = Person(80, 5, 1)
    screen.insertEntity(p)
    for i in range(25):
        p.move('right', screen.getCurrentScreen())
        screen.updateEntity(p)
        print(screen.render())
        time.sleep(0.1)
