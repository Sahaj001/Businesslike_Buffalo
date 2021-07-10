import numpy as np

class Line:
    def __init__(self, arr):
        self.array = arr
#    def display(self, pos):
        
        
from random import shuffle, randrange

class Maze:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.cells = []
        self.rows = np.zeros([self.width, self.height])
        self.lines = []
        
    # Create and display the maze
    def create_maze(self):
        h = self.height 
        w = self.width
        # Keep track of the cells that have already been explored
        seen = [[0] * w + [1] for a in range(h)] + [[1] * (w + 1)] 
        # Create vacant cells divided by walls
        cells = [["|  "] * w + ['|'] for a in range(h)] + [[]] 
        # Create horizontal walls
        wall = [["┼──"] * w + ['┼'] for a in range(h + 1)] 
        
        
        # Go around the empty grid to make paths and walls for the maze
        def explore(x, y):
            seen[y][x] = 1

            neighb = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(neighb)
            for (x1, y1) in neighb:
                if seen[y1][x1]: continue
                if x1 == x: wall[max(y, y1)][x] = "┼  "
                if y1 == y: cells[y][max(x, x1)] = "   "
                explore(x1, y1)

        explore(randrange(w), randrange(h))
        for (a, b) in zip(wall, cells):
            self.cells.append(a)
            self.cells.append(b)
            print(''.join(a + ['\n'] + b))
            
    # Make the sequence of line objects to represent the maze
    def make_lines(self):
        for row in self.cells:
            wid = (self.width*3)+1
            new_arr = np.zeros([1,wid])
            print(row)
            for ind, ch in enumerate(''.join(row)):
                for c in ch:
                    if c == '┼' or c == '─' or c == '|':
                        new_arr[0][ind] = 1
                    else:
                        new_arr[0][ind] = 0
                        
            print(new_arr)
            np.append(self.rows, new_arr)
            self.lines.append(Line(new_arr))
        print(self.rows)
                    

maz = Maze(10,5)
maz.create_maze()
maz.make_lines()
