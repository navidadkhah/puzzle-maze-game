import pygame
import sys
from maps.map import maze
from maps.fog import Fog_matrix
from maps.fog_entrance_locations import NORTH_ENTRANCE, SOUTH_ENTRANCE, WEST_ENTRANCE, EAST_ENTRANCE
from assets.colors import WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY, PURPLE, LIGHT_BLUE
from puzzles.ImpossibleMaze4 import impossible_maze
from puzzles.battle_ship import main_battle_ship
from puzzles.quizPuzzle import text_puzzle_question
from puzzles.quizWithHint import quiz_game_with_hint
from puzzles.cryptoGame import play_cipher_game
import copy

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

# Make sure to have an 'arrow.png' in your directory
arrow_image = pygame.image.load('Images/Arrow.jpg')
arrow_image = pygame.transform.scale(
    arrow_image, (cell_size, cell_size))  # Scale it to fit the cell


class Agent:
    def __init__(self, score):
        self.score = score
        self.bonus = 0
        self.fog_entrance = 0
        self.fog_entrance_capacity = 3
        self.player_x_before_fog = 0
        self.player_y_before_fog = 0
        self.is_in_fog = False
        self.game_maze = copy.deepcopy(maze)

    def draw_maze(self):
        for row in range(grid_size):
            for col in range(grid_size):
                if self.game_maze[row][col] == 0:
                    color = WHITE
                elif self.game_maze[row][col] == 2:
                    color = GRAY
                elif self.game_maze[row][col] == 3:
                    center_x = col * cell_size + cell_size // 2
                    center_y = row * cell_size + cell_size // 2
                    pygame.draw.circle(
                        screen, PURPLE, (center_x, center_y), cell_size // 3)
                    continue  # Skip drawing the rectangle to leave the bomb visible
                elif self.game_maze[row][col] == 4:
                    center_x = col * cell_size + cell_size // 2
                    center_y = row * cell_size + cell_size // 2
                    pygame.draw.circle(
                        screen, BLUE, (center_x, center_y), cell_size // 3)
                    continue  # Skip drawing the rectangle to leave the bomb visible
                elif self.game_maze[row][col] == 5:
                    color = YELLOW
                elif self.game_maze[row][col] == 6:
                    color = RED
                elif self.game_maze[row][col] == 7:
                    color = LIGHT_BLUE
                else:
                    color = BLACK
                pygame.draw.rect(
                    screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    def draw_player(self):
        # Draw player
        center_x = player_pos[1] * cell_size + cell_size // 2
        center_y = player_pos[0] * cell_size + cell_size // 2
        pygame.draw.circle(screen, GREEN, (center_x, center_y), cell_size // 2)
        # Draw entrance and exit
        screen.blit(arrow_image, (0 * cell_size, 11 * cell_size))
        screen.blit(arrow_image, (22 * cell_size, 11 * cell_size))

    def move_player(self, dx, dy, matrix_entrance):
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:

            if self.game_maze[new_x][new_y] != 1 \
                    and (new_x - 11 < 0 or new_x - 11 > 2 or new_y - 13 < 0 or new_y - 13 > 2):
                self.is_in_fog = False
                self.player_y_before_fog = 0
                self.player_x_before_fog = 0
                self.fog_entrance = 0

            if self.game_maze[new_x][new_y] == 0 or self.game_maze[new_x][new_y] == 5:
                self.score -= 10
                player_pos[0], player_pos[1] = new_x, new_y
                if not (player_pos[0] == NORTH_ENTRANCE[0] and player_pos[1] == NORTH_ENTRANCE[1]) \
                        and not (player_pos[0] == SOUTH_ENTRANCE[0] and player_pos[1] == SOUTH_ENTRANCE[1]) \
                        and not (player_pos[0] == EAST_ENTRANCE[0] and player_pos[1] == EAST_ENTRANCE[1]) \
                        and not (player_pos[0] == WEST_ENTRANCE[0] and player_pos[1] == WEST_ENTRANCE[1]):
                    matrix_entrance[new_x][new_y] += 1

                current_entrance = matrix_entrance[new_x][new_y]
                if current_entrance == 2:
                    self.game_maze[new_x][new_y] = 5
                    self.score -= 10
                if current_entrance == 3:
                    self.game_maze[new_x][new_y] = 6
                    self.score -= 30

            elif self.game_maze[new_x][new_y] == 2:
                print("Bia bazi")
                state = self.open_new_window(new_x, new_y)
                if state:
                    player_pos[0], player_pos[1] = new_x, new_y
            elif self.game_maze[new_x][new_y] == 3:
                print("Teleport - yellow")
                if new_x == 1:
                    player_pos[0], player_pos[1] = 21, 5
                else:
                    player_pos[0], player_pos[1] = 1, 15
            elif self.game_maze[new_x][new_y] == 4:
                print("Portal - blue")
                if new_x == 13:
                    player_pos[0], player_pos[1] = 3, 9
                else:
                    player_pos[0], player_pos[1] = 13, 15
            elif self.game_maze[new_x][new_y] == 7:
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

    def is_traped(self):
        if (self.game_maze[player_pos[0] + 1][player_pos[1]] == 1 or self.game_maze[player_pos[0] + 1][player_pos[1]] == 6) \
                and (self.game_maze[player_pos[0] - 1][player_pos[1]] == 1 or self.game_maze[player_pos[0] - 1][player_pos[1]] == 6) \
                and (self.game_maze[player_pos[0]][player_pos[1] + 1] == 1 or self.game_maze[player_pos[0]][player_pos[1] + 1] == 6) \
                and (self.game_maze[player_pos[0]][player_pos[1] - 1] == 1 or self.game_maze[player_pos[0]][player_pos[1] - 1] == 6):
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
                self.game_maze[dx][dy] = 0
                return True
            return False

        elif dx == 19 and dy == 6:
            score, is_done = main_battle_ship()
            temp_score = self.score + score
            if temp_score > 2000:
                self.bonus = self.score % 2000
                self.score = 2000
            else:
                self.score += score
            if is_done:
                self.game_maze[dx][dy] = 0
                return True
            return False

        elif dx == 4 and dy == 9:
            question = "آن چیست که هرچه از آن کم کنی بیشتر میشود؟"
            answer = text_puzzle_question(screen, question)
            if answer == "نمیدونم":
                temp_score = self.score + 60
                if temp_score > 2000:
                    self.bonus = self.score % 2000
                    self.score = 2000
                else:
                    self.score += 60
                    self.game_maze[dx][dy] = 0
                    return True
            else:
                self.score -= 10
                print("Incorrect answer. Try again!")
                return False

        elif dx == 18 and dy == 7:
            question = "معادله رو با حرکت یک چوب کبریت حل کن"
            answer = text_puzzle_question(
                screen, question, "./Images/kebrit.png")
            if answer == "142-3=139":
                temp_score = self.score + 60
                if temp_score > 2000:
                    self.bonus = self.score % 2000
                    self.score = 2000
                else:
                    self.score += 60
                self.game_maze[dx][dy] = 0
                return True
            else:
                self.score -= 10
                print("Incorrect answer. Try again!")
                return False

        elif dx == 13 and dy == 10:
            question = "خاور <- دبهز, بیمار <- ثپهتس, تاس <- جپص, داور <- ؟"
            hints = ["راهنمایی ۱: تست", "راهنمایی ۲: تست 2"]
            answer = quiz_game_with_hint(screen, question, "داور", hints)
            if answer == "داور":
                temp_score = self.score + 60
                if temp_score > 2000:
                    self.bonus = self.score % 2000
                    self.score = 2000
                else:
                    self.score += 60
                self.game_maze[dx][dy] = 0
                return True
            else:
                self.score -= 10
                print("Incorrect answer. Try again!")
                return False

        elif dx == 10 and dy == 9:
            question = "چهار مرد در یک صف ایستاده اند و بین مرد چهارم و سایر مردها، یک دیوار کشیده شده است. این مردان توانایی صحبت کردن با یکدیگر یا برگرداندن سرشان را ندارند و هرکسی فقط مرد یا مردان جلوی خود را میبیند. دیوار کشیده شده باعث میشود که مرد چهارم توسط هیچ کسی دیده نشود. همه مردان می دانند دو کلاه سفید و دو کلاه سیاه در بازی وجود دارد. کدام مرد زودتر میتواند رنگ کلاهش را حدس بزند؟"
            answer = text_puzzle_question(
                screen, question, "./Images/hat.png")

            if answer == "2":
                temp_score = self.score + 60
                if temp_score > 2000:
                    self.bonus = self.score % 2000
                    self.score = 2000
                else:
                    self.score += 60
                self.game_maze[dx][dy] = 0
                return True
            else:
                self.score -= 10
                print("Incorrect answer. Try again!")
                return False

        elif dx == 8 and dy == 15:
            question = "سه نفر در جزیره ی آدم خوارانِ منطقی گیر افتادند! آدم خواران اعلام کردند که یک فرصت برای نجات جان خود دارند، اما این تنها فرصت آن هاست. پنج کلاه مشابه که سه تای آنها سفید و دوتای آنها سیاه هستند بر روی میزی در برابر زندانیان قرار داشت. آدم خواران چشمان زندانیان را باز کردند. هر زندانی تنها کلاه افراد روبه روی خود را دید و نمی توانست کلاه خودش را ببیند. آدم خواران گفتند که اگر کسی رنگ کلاه خودش را به درستی اعلام کند، هر سه نفر نجات پیدا کرده و خورده نخواهند شد! آن ها از نفر آخر شروع به پرسیدن کردند. نفر آخر گفت: نمی دانم. و به سمت دیگ آب جوشحرکت کرد. نفر دوم هم گفت نمی دانم. و با غم به سمت دیگ راه افتاد. در این لحظه نفر سوم ناگهان فریاد زد: صبر کنید. من رنگ کلاه خودم را می دانم! کلاه او چه رنگی است؟"
            answer = text_puzzle_question(screen, question)
            if answer == "سفید":
                temp_score = self.score + 60
                if temp_score > 2000:
                    self.bonus = self.score % 2000
                    self.score = 2000
                else:
                    self.score += 60
                self.game_maze[dx][dy] = 0
                return True
            else:
                self.score -= 10
                print("Incorrect answer. Try again!")
                return False

        elif dx == 9 and dy == 12:
            original_size = screen.get_size()  # Store the current screen size
            score, is_done = play_cipher_game()  # Run the crypto game

            # After the crypto game ends, reset the game window size
            pygame.display.set_mode(original_size)  # Reset to the original game window size

            if is_done:
                self.score += score
                self.game_maze[dx][dy] = 0
                print(f"Cipher solved! Gained {score} points.")
                return True
            else:
                self.score -= 10  # Penalty for failure
                print("Failed to solve the cipher.")
                return False



def display_score(score):
    font = pygame.font.Font(None, 24)  # Use a default font with size 36
    text = font.render(f"Score: {score}", True, WHITE)  # Create a text surface
    screen.blit(text, (screen_size - 100, 10))  # Draw the text at the top-right


def play_game():
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
                    agent.move_player(-1, 0, matrix_entrance)
                elif event.key == pygame.K_DOWN:
                    agent.move_player(1, 0, matrix_entrance)
                elif event.key == pygame.K_LEFT:
                    agent.move_player(0, -1, matrix_entrance)
                elif event.key == pygame.K_RIGHT:
                    agent.move_player(0, 1, matrix_entrance)

        # Draw maze and player
        screen.fill(WHITE)
        agent.draw_maze()
        agent.draw_player()
        display_score(agent.score)
        pygame.display.flip()

        if player_pos == [11, 21]:
            agent.score += 2000
            if agent.bonus > 0:
                agent.score += agent.bonus
            score = min(4000, agent.score)
            print(score)

            level = ""
            if 3750 < score < 4000:
                level = "S"
            elif 3650 < score < 3749:
                level = "A"
            elif 3400 < score < 3649:
                level = "B"
            elif 0 < score < 3400:
                level = "C"

            note = "You successfully completed the maze!!!"
            print(f"Your rank is {level}")

            return note, level, score

        if agent.is_traped():
            note = "You are trapped"
            level = "C"
            return note, level, agent.score

    pygame.quit()
    sys.exit()
