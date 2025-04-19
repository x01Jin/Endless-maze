import pygame
from maze import Maze
from player import Player
from coins import Coins
from timer import Timer

GRID_SIZE = 32
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CELL_SIZE = min(WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE)
GRID_DRAW_SIZE = CELL_SIZE * GRID_SIZE
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_DRAW_SIZE) // 2
GRID_OFFSET_Y = (WINDOW_HEIGHT - GRID_DRAW_SIZE) // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
YELLOW = (255, 215, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (220, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Endless Maze")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

def draw_maze(maze, player, coins, exit_pos):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.grid.grid[y, x] == 0:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
    for pos in coins.positions:
        if pos not in coins.collected:
            pygame.draw.circle(screen, YELLOW, (GRID_OFFSET_X + pos[0] * CELL_SIZE + CELL_SIZE // 2, GRID_OFFSET_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.rect(screen, GREEN, (GRID_OFFSET_X + exit_pos[0] * CELL_SIZE, GRID_OFFSET_Y + exit_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.circle(screen, BLUE, (GRID_OFFSET_X + player.pos[0] * CELL_SIZE + CELL_SIZE // 2, GRID_OFFSET_Y + player.pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def draw_ui(timer, coins, level):
    t = font.render(f"Time: {timer.time_left}", True, RED if timer.time_left <= 10 else WHITE)
    c = font.render(f"Coins: {len(coins.collected)}/3", True, YELLOW)
    l = font.render(f"Level: {level}", True, WHITE)
    screen.blit(t, (10, 10))
    screen.blit(c, (10, 40))
    screen.blit(l, (10, 70))

def main():
    level = 1
    maze = Maze(level)
    player = Player(maze)
    coins = Coins(maze)
    timer = Timer()
    running = True
    game_over = False

    move_dir = None
    move_timer = 0

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        move_dir = 'w'
                    elif event.key == pygame.K_a:
                        move_dir = 'a'
                    elif event.key == pygame.K_s:
                        move_dir = 's'
                    elif event.key == pygame.K_d:
                        move_dir = 'd'
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                        if ((event.key == pygame.K_w and move_dir == 'w') or
                            (event.key == pygame.K_a and move_dir == 'a') or
                            (event.key == pygame.K_s and move_dir == 's') or
                            (event.key == pygame.K_d and move_dir == 'd')):
                            move_dir = None

        if not game_over:
            timer.update()
            if move_dir:
                move_timer += dt
                while move_timer >= 0.1:
                    player.move(move_dir)
                    coins.collect(player.pos)
                    move_timer -= 0.1
            else:
                move_timer = 0
            if coins.all_collected() and player.pos == maze.exit_pos:
                level += 1
                maze = Maze(level)
                player = Player(maze)
                coins = Coins(maze)
                timer.reset()
            if timer.is_time_up():
                game_over = True
        screen.fill(BLACK)
        draw_maze(maze, player, coins, maze.exit_pos)
        draw_ui(timer, coins, level)
        if game_over:
            msg = font.render("Game Over", True, RED)
            screen.blit(msg, (WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 - 20))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
