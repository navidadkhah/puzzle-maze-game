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

class Agent:
    def __init__(self, score):
        self.score = score
        self.bonus = 0

    def draw_maze(self):
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

    def draw_player(self):
        pygame.draw.rect(screen, GREEN, (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

    def move_player(self, dx, dy):
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if maze[new_x][new_y] == 0 or maze[new_x][new_y] == 5:
                self.score -= 10
                player_pos[0], player_pos[1] = new_x, new_y
                matrix[new_x][new_y] += 1
                current_entrance = matrix[new_x][new_y]
                if current_entrance == 2:
                    maze[new_x][new_y] = 5
                    self.score -= 10
                if current_entrance == 3:
                    maze[new_x][new_y] = 6
                    self.score -= 30
            elif maze[new_x][new_y] == 2:
                print("Bia bazi")
                self.open_new_window()
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
        print(self.score)

    def open_new_window(self):
        # Create a new window
        new_screen = pygame.display.set_mode((300, 300))
        new_screen.fill(BLUE)
        pygame.display.set_caption("Mini Game")
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        waiting_for_key = False
        # Reset to original screen size
        pygame.display.set_mode((screen_size, screen_size))


# Game loop
running = True

matrix = []
score = 2000


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

agent = Agent(score)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                agent.move_player(-1, 0)
            elif event.key == pygame.K_DOWN:
                agent.move_player(1, 0)
            elif event.key == pygame.K_LEFT:
                agent.move_player(0, -1)
            elif event.key == pygame.K_RIGHT:
                agent.move_player(0, 1)

    # Draw maze and player
    screen.fill(WHITE)
    agent.draw_maze()
    agent.draw_player()
    pygame.display.flip()

    if player_pos == [11, 21]:
        running = False
        if agent.bonus > 0:
            score = agent.score + agent.bonus
        score = min(4000, agent.score + agent.bonus)

        if score > 3750 and score < 4000:
            level = "S"
        elif score > 3650 and score < 3749:
            level = "A"
        elif score > 3400 and score < 3649:
            level = "B"
        elif score > 0 and score < 3400:
            level = "C"


        print("You successfully completed the maze!!!")
        print(f"Your rank is {level}")

pygame.quit()
sys.exit()
