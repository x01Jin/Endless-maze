class Coins:
    def __init__(self, maze):
        self.maze = maze
        self.positions = list(maze.coin_positions)
        self.collected = set()

    def collect(self, pos):
        if pos in self.positions and pos not in self.collected:
            self.collected.add(pos)

    def all_collected(self):
        return len(self.collected) == 3

    def reset(self):
        self.positions = list(self.maze.coin_positions)
        self.collected.clear()
