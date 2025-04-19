from maze import Maze

DIRECTIONS = {
    'w': (0, -1),
    'a': (-1, 0),
    's': (0, 1),
    'd': (1, 0)
}

class Player:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.pos = maze.player_pos
        self.collected = set()

    def move(self, direction):
        if direction not in DIRECTIONS:
            return
        dx, dy = DIRECTIONS[direction]
        x, y = self.pos
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.maze.grid.grid.shape[1] and 0 <= ny < self.maze.grid.grid.shape[0]:
            if self.maze.grid.is_path(nx, ny):
                self.pos = (nx, ny)
                self.collect_coin()

    def collect_coin(self):
        if self.pos in self.maze.coin_positions and self.pos not in self.collected:
            self.collected.add(self.pos)

    def reset(self):
        self.pos = self.maze.player_pos
        self.collected.clear()
