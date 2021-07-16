from entities import Bar, CampFire, Fountain, Grass, House, Lake, Tent, Tree, WitchHut


class Map:
    def __init__(self):
        self.map_1 = []

    def map_initialise(self):
        for grass_col in range(2):
            for grass_row in range(6):
                self.map_1.append((Grass(68+(10*grass_col), grass_row*4, 5, f"Grass{grass_row}{grass_col}"), True))
        for grass_col in range(36, 65, 10):
            self.map_1.append((Grass(grass_col, 0, 5, f"Grass up{grass_col}"), True))
            for grass_row in range(15, 23, 4):
                self.map_1.append((Grass(grass_col, grass_row, 5, f"Grass down{grass_col}"), True))
        self.map_1.append((Tent(58, 7, 5, "Upper Central Tent"), False))
        self.map_1.append((CampFire(58, 11, 5, "Central Campfire"), False))
        self.map_1.append((Tent(53, 11, 5, "Right Central Tent"), False))
        self.map_1.append((Tent(63, 11, 5, "Left Central Tent"), False))
        self.map_1.append((Tent(58, 14, 5, "Bottom Central Tent"), False))
        self.map_1.append((Lake(0, 0, 5, "Top Left Lake"), True))
        for tree_col in range(3):
            for tree_row in range(8):
                self.map_1.append((Tree(1 + tree_row * 5, 6 + (4 * tree_col), 5, f"Tree{tree_row}{tree_col}"), False))
        self.map_1.append((Lake(0, 18, 5, "Bottom Left lake"), True))
