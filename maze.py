import numpy as np
import random
from grid import Grid, PATH, WALL, GRID_SIZE

class Maze:
    def __init__(self, level=1):
        self.level = level
        self.grid = Grid()
        self.player_pos = None
        self.exit_pos = None
        self.coin_positions = []
        self.generate_maze()

    def generate_maze(self):
        self.grid.grid[:, :] = WALL
        stack = []
        x, y = random.randrange(0, GRID_SIZE, 2), random.randrange(0, GRID_SIZE, 2)
        self.grid.set_cell(x, y, PATH)
        stack.append((x, y))
        last_dir = None
        while stack:
            cx, cy = stack[-1]
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid.get_cell(nx, ny) == WALL:
                    neighbors.append((nx, ny, dx, dy))
            if neighbors:
                if self.level == 1:
                    if last_dir:
                        straight = [n for n in neighbors if (n[2], n[3]) == last_dir]
                        if straight and random.random() < 0.8:
                            nx, ny, dx, dy = random.choice(straight)
                        else:
                            nx, ny, dx, dy = random.choice(neighbors)
                    else:
                        nx, ny, dx, dy = random.choice(neighbors)
                    last_dir = (dx, dy)
                else:
                    nx, ny, dx, dy = random.choice(neighbors)
                    last_dir = (dx, dy)
                self.grid.set_cell(cx + dx // 2, cy + dy // 2, PATH)
                self.grid.set_cell(nx, ny, PATH)
                stack.append((nx, ny))
            else:
                stack.pop()
        self.place_player_exit_coins()

    def place_player_exit_coins(self):
        def is_reachable(start, targets):
            from collections import deque
            visited = set()
            queue = deque([start])
            found = set()
            while queue:
                x, y = queue.popleft()
                if (x, y) in targets:
                    found.add((x, y))
                    if len(found) == len(targets):
                        return True
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if self.grid.get_cell(nx, ny) == PATH and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
            return False

        path_cells = [tuple(cell) for cell in np.argwhere(self.grid.grid == PATH)]
        if len(path_cells) < 5:
            raise ValueError("Not enough path cells to place player, exit, and coins.")

        max_attempts = 100
        for _ in range(max_attempts):
            selected = random.sample(path_cells, 5)
            player = selected[0]
            exit_ = selected[1]
            coins = [pos for pos in selected[2:] if self.grid.get_cell(pos[0], pos[1]) == PATH]
            needed = 3 - len(coins)
            if needed > 0:
                remaining = [cell for cell in path_cells if cell not in selected and self.grid.get_cell(cell[0], cell[1]) == PATH]
                coins += random.sample(remaining, needed)
            targets = set([exit_] + coins)
            if is_reachable(player, targets):
                self.player_pos = player
                self.exit_pos = exit_
                self.coin_positions = coins
                return
        raise RuntimeError("Failed to place player, coins, and exit with connectivity after many attempts.")

    def reset(self, level=None):
        if level is not None:
            self.level = level
        self.generate_maze()
