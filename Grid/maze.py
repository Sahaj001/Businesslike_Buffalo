from random import shuffle, randrange

import numpy as np

class Maze:
    '''
    A class that randomly generates a maze with a set width and height.
    It can be represented in text(cells) and numpy array form(rows)
    '''
    
    # Initialize values of the maze object
    def __init__(self, width, height):
        self.height: int = height
        self.width: int = width
        self.cells = []
        self.rows = self.make_lines()

    # Create and display the maze
    def create_maze(self):
        h: int = self.height
        w: int = self.width
        # Keep track of the cells that have already been explored
        seen = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        # Create vacant cells divided by walls
        cells = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        # Create horizontal walls
        wall = [["┼──"] * w + ['┼'] for _ in range(h + 1)]

        # Go around the empty grid to make paths and walls for the maze
        def explore(x: int, y: int):
            seen[y][x] = 1
            
            # Go over the neighboring cells in the maze and shuffle them
            neighbor = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(neighbor)
           
            for (x1: int, y1: int) in neighbor:
                # If the selected cell has been explored, ignore it
                if seen[y1][x1]: 
                    continue
                # Place a wall on the randomly selected side when moving horizontally
                if x1 == x:
                    wall[max(y, y1)][x] = "┼  "
                # Make a path on the randomly selected side when moving vertically
                if y1 == y:
                    cells[y][max(x, x1)] = "   "
                explore(x1, y1)

        # Start the exploration on a random position on the empty grid
        explore(randrange(w), randrange(h))
        # Make the ascii form of the maze and store it in self.cells
        for (a, b) in zip(wall, cells):
            self.cells.append(a)
            self.cells.append(b)
            print(''.join(a + ['\n'] + b))

    # Make the sequence of line objects to represent the maze
    def make_lines(self):
        # Empty list to contain the arrays
        array_ = []
        # Go over all the ascii rows of the maze
        for row in self.cells:
            wid: int = (self.width * 3) + 1
            # Make a 1D array full of zeros to be edited and represent occupied and vacant spaces
            new_arr = np.zeros([1, wid])
            # Ignore if the row is empty
            if not row:
                continue
            # Join the characters of the row into one string 
            for ind, ch in enumerate(''.join(row)):
               # Loop over each character in the string
                for c in ch:
                    # Represent 'wall' characters as 1s or occupied spaces
                    if c == '┼' or c == '─' or c == '|':
                        new_arr[0][ind] = 1
                    # Keep them as 0s if they're blank/vacant
                    else:
                        continue
            # Add the edited array object to a list
            array_.append(new_arr)
        # Flatten the arrays in the list into 1 long numpy array
        array_1 = np.array(array_).flatten()
        # Return a 2D array representation of the maze made out of 1s and 0s
        try:
            new_array_ = np.reshape(array_1, (11, 31))
            return new_array_
        except ValueError:
            return array_1
