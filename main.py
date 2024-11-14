import pygame
import sys
from map import maze
from colors import WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY, PURPLE

# Initialize Pygame
pygame.init()
# Set up display
cell_size = 20  # Size of each cell in the grid
grid_size = 23  # Size of the maze (9x9)

screen_size = grid_size * cell_size
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("9x9 Maze Game")

# Player starting position
player_pos = [11, 1]

def draw_maze():
    for row in range(grid_size):
        for col in range(grid_size):
            if maze[row][col] == 0:
                color = WHITE
            elif maze[row][col] == 2:
                color = GRAY
            elif maze[row][col] == 3:
                color = PURPLE
            elif maze[row][col] == 4:
                color = BLUE
            elif maze[row][col] == 5:
                color = YELLOW
            elif maze[row][col] == 6:
                color = RED
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < grid_size and 0 <= new_y < grid_size:

        if maze[new_x][new_y] == 0 or maze[new_x][new_y] == 5:
            player_pos[0], player_pos[1] = new_x, new_y
            matrix[new_x][new_y] += 1
            print(matrix[new_x][new_y])
            current_entrance = matrix[new_x][new_y]
            if current_entrance == 2:
                print("here 2")
                maze[new_x][new_y] = 5
            if current_entrance == 3:
                print("here 3")
                maze[new_x][new_y] = 6

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

matrix = []

for row in range(grid_size):
    a = []
    for column in range(grid_size):
        a.append(0)
    matrix.append(a)

# # For printing the matrix
# for row in range(grid_size):
#     for column in range(grid_size):
#         print(matrix[row][column], end=" ")
#     print()

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
