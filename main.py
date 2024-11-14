import pygame
import sys
from map import maze

# Initialize Pygame
pygame.init()
# Set up display
cell_size = 20  # Size of each cell in the grid
grid_size = 23  # Size of the maze (9x9)
screen_size = grid_size * cell_size
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("9x9 Maze Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)



# Player starting position
player_pos = [11, 1]

def draw_maze():
    for row in range(grid_size):
        for col in range(grid_size):
            if maze[row][col] == 0:
                color = WHITE
            elif maze[row][col] == 2:
                color = RED
            elif maze[row][col] == 3:
                color = YELLOW
            elif maze[row][col] == 4:
                color = BLUE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
        if maze[new_x][new_y] == 0:
            player_pos[0], player_pos[1] = new_x, new_y
        elif maze[new_x][new_y] == 2:
            print("Bia bazi")
            player_pos[0], player_pos[1] = new_x, new_y
        elif maze[new_x][new_y] == 3:
            print("Teleport - yellow")
            if new_x == 1:
                player_pos[0], player_pos[1] = 21, 5
            else:
                player_pos[0], player_pos[1] = 1, 15

        elif maze[new_x][new_y] == 4:
            print("Teleport - blue")
            if new_x == 13:
                player_pos[0], player_pos[1] = 3, 9
            else:
                player_pos[0], player_pos[1] = 13, 15


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(-1, 0)
            elif event.key == pygame.K_DOWN:
                move_player(1, 0)
            elif event.key == pygame.K_LEFT:
                move_player(0, -1)
            elif event.key == pygame.K_RIGHT:
                move_player(0, 1)

    # Draw maze and player
    screen.fill(WHITE)
    draw_maze()
    draw_player()
    pygame.display.flip()

pygame.quit()
sys.exit()
