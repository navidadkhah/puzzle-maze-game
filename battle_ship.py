import pygame
import sys

# Constants for the grid
CELL_SIZE = 40
GRID_SIZE = 10
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 200)


def init():
    global screen, clock, cell_states
    # Initialize Pygame
    pygame.init()
    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid Tap Game")
    # Clock
    clock = pygame.time.Clock()
    # Initialize grid state (all cells start as BLACK)
    cell_states = [[BLUE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = cell_states[row][col]
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw border


def get_cell_pos(mouse_pos):
    x, y = mouse_pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return (row, col)


def toggle_cell_color(pos):
    row, col = pos
    current_color = cell_states[row][col]
    new_color = BLUE if current_color == RED else RED
    cell_states[row][col] = new_color


def main_battle_ship():
    init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell_pos = get_cell_pos(pos)
                toggle_cell_color(cell_pos)

        screen.fill(RED)
        draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


