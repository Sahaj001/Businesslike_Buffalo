from random import shuffle, randrange, randint

import numpy as np

class Maze:
    '''
    A class that randomly generates a maze with a set width and height.
    It can be represented in text(cells) and numpy array form(rows)
    '''
    
    # Initialize values of the maze object
    def __init__(self, width:int, height:int, num_keys:int) -> None:
        self.height: int = height
        self.width: int = width
        self.num_keys: int = num_keys
        self.cells = []
        self.create_maze()
        self.make_lines()
        self.spawn_and_key()

    # Create and display the maze
    def create_maze(self) -> None:
        h: int = self.height
        w: int = self.width
        # Keep track of the cells that have already been explored
        seen = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        # Create vacant cells divided by walls
        cells = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        # Create horizontal walls
        wall = [["┼──"] * w + ['┼'] for _ in range(h + 1)]

        # Go around the empty grid to make paths and walls for the maze
        def explore(x:int, y:int) -> None:
            seen[y][x] = 1
            
            # Go over the neighboring cells in the maze and shuffle them
            neighbor = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(neighbor)
           
            for (x1:int, y1:int) in neighbor:
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
    def make_lines(self) -> np.ndarray:
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
        # Return a 2D array representation of the maze made out of 1s and 0s and make the numpy matrix representation of the maze
        try:
            new_array_ = np.reshape(array_1, (11, 31))
            self.rows = new_array_
            return new_array_ 
        except ValueError:
            self.rows = array_1
            return array_1
        
    # Initialize locations for the player's spawn point and the objective
    def spawn_and_key(self) -> None:
        # Get the cells(ascii) and rows(num) of the maze
        cells = self.cells
        rows = self.rows
        # Get the horizontal and vertical range of spaces in the maze 
        hor_range = range(1,len(cells[0])-1)
        ver_range = range(1,len(cells)-1)
        # Select a random row along the y axis for spawn and key
        y_pos_spawn = randint(1, ver_range[-1])
        # Randomly generate 3 key positions
        y_pos_keys = []
        for n in range(self.num_keys):
            y_pos_keys.append(randint(1, ver_range[-1]))
        # Keep track of whether valid spawn or key positions have been found or not
        key_pos = False
        # Make function that finds a valid position
        def find_pos(a_range: range, y_pos: int):
            # Go over all the cells in the row to find a vacant position
            pos_found = False
            while pos_found == False:
                pos = randint(1, a_range[-1])
                # Exit the while loop if a valid position is found
                if self.rows[y_pos][pos] == 0:
                    pos_found = True
            return pos
        # Make tuples representing the positions of the spawn and key in the maze
        spawn_pos = (y_pos_spawn, find_pos(ver_range, y_pos_spawn))
        # Represent the spawn point with a 3 in the numpy array and a * in the ascii
        self.rows[spawn_pos[0]][spawn_pos[1]] = 2
        # Place the keys in their respective places
        for key in y_pos_keys:
            key_pos = (key, find_pos(hor_range, key))
            self.rows[key_pos[0]][key_pos[1]] = 3
            key_cells = list(''.join(cells[key]))  
            key_cells[key_pos[1]] = 'K'
            self.cells[key] = key_cells
        # Represent the key and spawn points on the cells attribute
        spawn_cells = list(''.join(cells[y_pos_spawn]))
        spawn_cells[spawn_pos[1]:int] = '@'
        # Update the row and cells in the maze
        self.cells[y_pos_spawn:int] = spawn_cells

    # Display the maze
    def display(self) -> None:
        empty = []
        # Join the sequence of characters into one list
        for row in self.cells:
            new_row = ''.join(row)
            empty.append(new_row)
        print('\n'.join(empty))
