import pygame
import random

WIDTH, HEIGHT = 920, 600
CELL_SIZE = 40
GRID_WIDTH = (WIDTH // CELL_SIZE) // 2 * 2 + 1
GRID_HEIGHT = (HEIGHT // CELL_SIZE) // 2 * 2 + 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MOVEMENT_SPEED = 200

class Dungeon:
    def __init__(self):
        self.level = 1
        self.generate_maze()
        self.player_x, self.player_y = 1, 1
        self.regenerate_maze = False
        self.last_move_time = 0
        self.move_delay = MOVEMENT_SPEED

    def generate_maze(self):
        self.map = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            self.map[y][x] = True
            unvisited_neighbors = []
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < GRID_WIDTH - 1 and 0 < ny < GRID_HEIGHT - 1 and not self.map[ny][nx]:
                    unvisited_neighbors.append((nx, ny))
            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                wall_x, wall_y = (next_x + x) // 2, (next_y + y) // 2
                self.map[wall_y][wall_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        # Generate keys and goal in white tiles only
        available_tiles = [(x, y) for y in range(1, GRID_HEIGHT - 1) for x in range(1, GRID_WIDTH - 1) if self.map[y][x]]
        random.shuffle(available_tiles)
        self.keys = [Key(*available_tiles.pop()) for _ in range(3)]
        self.goal_x, self.goal_y = available_tiles.pop()

    def draw(self, screen):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                color = WHITE if cell else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the keys
        for key in self.keys:
            pygame.draw.rect(screen, (255, 255, 0), (key.x * CELL_SIZE, key.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, (self.goal_x * CELL_SIZE, self.goal_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 0, 255), (self.player_x * CELL_SIZE, self.player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(text, (WIDTH - 150, 20))

    def move(self, dx, dy):
        if self.regenerate_maze:
            self.level += 1
            self.generate_maze()
            self.regenerate_maze = False

        current_time = pygame.time.get_ticks()
        if self.can_move(current_time):
            new_x, new_y = self.player_x + dx, self.player_y + dy
            if self.is_within_bounds(new_x, new_y):
                if self.collect_key(new_x, new_y):
                    return
                if self.reach_goal(new_x, new_y):
                    return

    def can_move(self, current_time):
        if current_time - self.last_move_time <= self.move_delay:
            return False
        return True

    def is_within_bounds(self, new_x, new_y):
        return 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT

    def collect_key(self, new_x, new_y):
        for key in self.keys:
            if new_x == key.x and new_y == key.y:
                self.keys.remove(key)
                return True
        return False

    def reach_goal(self, new_x, new_y):
        if new_x == self.goal_x and new_y == self.goal_y and not self.keys:
            self.regenerate_maze = True
        if self.map[new_y][new_x]:
            self.player_x, self.player_y = new_x, new_y
            self.last_move_time = pygame.time.get_ticks()

class Key:
    def __init__(self, x, y):
        self.x, self.y = x, y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Maze Game")
dungeon = Dungeon()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move = (keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
    dungeon.move(*move)

    screen.fill((0, 0, 0))
    dungeon.draw(screen)
    pygame.display.flip()

pygame.quit()