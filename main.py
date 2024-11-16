import pygame
import sys
from map import maze
from fog import Fog_matrix
from colors import WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY, PURPLE, LIGHT_BLUE
from ImpossibleMaze4 import impossible_maze

# Initialize Pygame
pygame.init()
# Set up display
cell_size = 20  # Size of each cell in the grid
grid_size = 23  # Size of the maze (9x9)

screen_size = grid_size * cell_size
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("9x9 Maze Game")

# Using blit to copy content from one surface to other

# Player starting position
player_pos = [10, 13]

arrow_image = pygame.image.load('Images/Arrow.jpg')  # Make sure to have an 'arrow.png' in your directory
arrow_image = pygame.transform.scale(arrow_image, (cell_size, cell_size))  # Scale it to fit the cell


class Agent:
    def __init__(self, score):
        self.score = score
        self.bonus = 0
        self.fog_entrance = 0
        self.fog_entrance_capacity = 3
        self.player_x_before_fog = 0
        self.player_y_before_fog = 0
        self.is_in_fog = False

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
                elif maze[row][col] == 7:
                    color = LIGHT_BLUE
                else:
                    color = BLACK
                pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    def draw_player(self):
        # Draw player
        center_x = player_pos[1] * cell_size + cell_size // 2
        center_y = player_pos[0] * cell_size + cell_size // 2
        pygame.draw.circle(screen, GREEN, (center_x, center_y), cell_size // 2)
        # Draw entrance and exit
        screen.blit(arrow_image, (0 * cell_size, 11 * cell_size))
        screen.blit(arrow_image, (21 * cell_size, 11 * cell_size))

    def move_player(self, dx, dy):
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if new_x - 11 < 0 or new_x - 11 > 2 or new_y - 13 < 0 or new_y - 13 > 2:
                self.is_in_fog = False
                self.player_y_before_fog = 0
                self.player_x_before_fog = 0
                self.fog_entrance = 0

            if maze[new_x][new_y] == 0 or maze[new_x][new_y] == 5:
                self.score -= 10
                player_pos[0], player_pos[1] = new_x, new_y
                matrix_entrance[new_x][new_y] += 1
                current_entrance = matrix_entrance[new_x][new_y]
                if current_entrance == 2:
                    maze[new_x][new_y] = 5
                    self.score -= 10
                if current_entrance == 3:
                    maze[new_x][new_y] = 6
                    self.score -= 30
            elif maze[new_x][new_y] == 2:
                self.is_in_fog = False
                self.fog_entrance += 1
                print("Bia bazi")
                state = self.open_new_window(new_x, new_y)
                if state:
                    player_pos[0], player_pos[1] = new_x, new_y
            elif maze[new_x][new_y] == 3:
                self.is_in_fog = False
                self.fog_entrance += 1
                print("Teleport - yellow")
                if new_x == 1:
                    player_pos[0], player_pos[1] = 21, 5
                else:
                    player_pos[0], player_pos[1] = 1, 15
            elif maze[new_x][new_y] <= 4:
                self.is_in_fog = False
                self.fog_entrance += 1
                print("Portal - blue")
                if new_x == 13:
                    player_pos[0], player_pos[1] = 3, 9
                else:
                    player_pos[0], player_pos[1] = 13, 15
            elif maze[new_x][new_y] == 7:
                if self.fog_entrance == 0 or not self.is_in_fog:
                    self.is_in_fog = True
                    self.fog_entrance += 1
                    self.player_x_before_fog = player_pos[1]
                    self.player_y_before_fog = player_pos[0]

                if self.fog_entrance <= self.fog_entrance_capacity:
                    self.score -= 10
                    if Fog_matrix[new_x - 11][new_y - 13] == 0:
                        self.fog_entrance += 1
                        player_pos[0], player_pos[1] = new_x, new_y
                    elif Fog_matrix[new_x - 11][new_y - 13] == 1:
                        print("There is a wall here")
                    elif Fog_matrix[new_x - 11][new_y - 13] == 4:
                        player_pos[0], player_pos[1] = 3, 9
                else:
                    player_pos[0], player_pos[1] = self.player_y_before_fog, self.player_x_before_fog
                    self.player_y_before_fog = 0
                    self.player_x_before_fog = 0
                    self.fog_entrance = 0
                    self.is_in_fog = False

        print(self.score)

    def is_traped(self):
        if (maze[player_pos[0] + 1][player_pos[1]] == 1 or maze[player_pos[0] + 1][player_pos[1]] == 6) \
                and (maze[player_pos[0] - 1][player_pos[1]] == 1 or maze[player_pos[0] - 1][player_pos[1]] == 6) \
                and (maze[player_pos[0]][player_pos[1] + 1] == 1 or maze[player_pos[0]][player_pos[1] + 1] == 6) \
                and (maze[player_pos[0]][player_pos[1] - 1] == 1 or maze[player_pos[0]][player_pos[1] - 1] == 6):
            return True
        else:
            return False

    def open_new_window(self, dx, dy):
        if dx == 8 and dy == 5:
            score, is_done = impossible_maze()
            temp_score = self.score + score
            if temp_score > 2000:
                self.bonus = self.score % 2000
                self.score = 2000
            else:
                self.score += score
            if is_done:
                maze[dx][dy] = 0
                return True
            return False


# Game loop
running = True
matrix_entrance = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

score = 2000
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
        score = agent.score + 2000
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

    if agent.is_traped():
        running = False
        print("You are a loser")

pygame.quit()
sys.exit()
