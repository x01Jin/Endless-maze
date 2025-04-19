import numpy as np

GRID_SIZE = 32
WALL = 0
PATH = 1

class Grid:
    def __init__(self):
        self.grid = np.full((GRID_SIZE, GRID_SIZE), WALL, dtype=np.uint8)

    def set_cell(self, x, y, value):
        self.grid[y, x] = value

    def get_cell(self, x, y):
        return self.grid[y, x]

    def is_path(self, x, y):
        return self.grid[y, x] == PATH

    def random_path_cell(self):
        ys, xs = np.where(self.grid == PATH)
        idx = np.random.randint(len(xs))
        return xs[idx], ys[idx]
