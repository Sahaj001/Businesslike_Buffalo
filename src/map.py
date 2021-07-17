from entities import Bar, CampFire, Grass, Lake, Tent, Tree, WitchHut


class Map:
    """Class responsible for rendering the map"""

    def __init__(self):
        self.map_1 = []
        self.map_2 = []
        self.map_3 = []

    def map_initialise(self) -> None:
        """Initialize the all the Entity Objects"""
        for grass_col in range(2):
            x_coord = 68 + (10 * grass_col)
            for grass_row in range(6):
                y_coord = grass_row * 4
                self.map_1.append((Grass(x_coord, y_coord, 5, f"Grass{grass_row}{grass_col}"), True, 5))

        for grass_col in range(36, 65, 10):
            self.map_1.append((Grass(grass_col, 0, 5, f"Grass up{grass_col}"), True, 5))
            for grass_row in range(15, 23, 4):
                self.map_1.append((Grass(grass_col, grass_row, 5, f"Grass down{grass_col}"), True, 5))

        self.map_1.append((Tent(58, 7, 5, "Upper Central Tent"), False, 5))
        self.map_1.append((CampFire(58, 11, 5, "Central Campfire"), False, 5))
        self.map_1.append((Tent(53, 11, 5, "Right Central Tent"), False, 5))
        self.map_1.append((Tent(63, 11, 5, "Left Central Tent"), False, 5))
        self.map_1.append((Tent(58, 14, 5, "Bottom Central Tent"), False, 5))

        for tree_row in range(3):
            x_coord_offset = 3 if tree_row % 2 == 1 else 0
            y_coord = 1 + (4 * tree_row)
            for tree_col in range(8):
                x_coord = 1 + tree_col * 5 + x_coord_offset
                self.map_1.append((Tree(x_coord, y_coord,
                                   5,
                                   f"Tree{tree_col}{tree_row}"),
                                   False,
                                   5))

        self.map_1.append((Lake(0, 15, 5, "Bottom Left lake"), True, 5))

        self.map_2.append((WitchHut(60, 10, 4, "Witch Hut"), False, 4))

        self.map_3.append((Bar(20, 10, 6, "Bar"), False, 6))
