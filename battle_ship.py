import random
import pygame
import sys

# Constants
CELL_SIZE = 40
GRID_SIZE = 10
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE
FPS = 60

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Battleship:

    def __init__(self):
        self.alive_ship = 4
        self.bombs = 0
        self.fail = False
        global screen, clock, alive_ship
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleship Game")
        clock = pygame.time.Clock()

    def draw_grid(self, hit_matrix, ship_matrix):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = hit_matrix[row][col]
                if cell == 'hit':
                    color = RED
                elif cell == 'miss':
                    color = WHITE
                elif cell == 'sunk':
                    color = BLACK
                elif cell == 'bomb':
                    center_x = col * CELL_SIZE + CELL_SIZE // 2
                    center_y = row * CELL_SIZE + CELL_SIZE // 2
                    pygame.draw.circle(screen, RED, (center_x, center_y), CELL_SIZE // 3)
                    continue  # Skip drawing the rectangle to leave the bomb visible
                else:
                    color = BLUE  # Unrevealed water
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def check_free(self, grid, row, col, ship, orientation):
        start_row = max(row - 1, 0)
        end_row = min(row + (ship if orientation == 'vertical' else 1) + 1, GRID_SIZE)
        start_col = max(col - 1, 0)
        end_col = min(col + (ship if orientation == 'horizontal' else 1) + 1, GRID_SIZE)

        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if grid[r][c] != 0:
                    return False
        return True


    def place_ship(self, grid, row, col, ship, orientation, ship_id):
        for i in range(ship):
            if orientation == 'horizontal':
                grid[row][col + i] = ship_id
            else:
                grid[row + i][col] = ship_id

    def random_ships(self):
        ship_lengths = [4, 3, 2, 1]
        grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        ship_id = 4  # Unique identifier for each ship

        for ship in ship_lengths:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    row = random.randint(0, GRID_SIZE - 1)
                    col = random.randint(0, GRID_SIZE - ship)
                else:
                    row = random.randint(0, GRID_SIZE - ship)
                    col = random.randint(0, GRID_SIZE - 1)

                if self.check_free(grid, row, col, ship, orientation):
                    self.place_ship(grid, row, col, ship, orientation, ship_id)
                    placed = True
            ship_id -= 1  # Increment the ship identifier for the next ship

        self.palce_bombs(grid)

        return grid

    def palce_bombs(self, grid):
        placed = 0
        while placed != 2:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)

            if self.check_free(grid, row, col, 1, "horizontal"):
                self.place_ship(grid, row, col, 1, "horizontal", 5)
                print(row)
                print(col)
                print("----")
                placed += 1
        print("added")


    def get_cell_pos(self, mouse_pos):
        x, y = mouse_pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        return (row, col)

    def handle_click(self, hit_matrix, ship_matrix, row, col):
        if ship_matrix[row][col] == 0:
            hit_matrix[row][col] = 'miss'
        elif ship_matrix[row][col] == 5:
            hit_matrix[row][col] = 'bomb'
            self.bombs += 1
            if self.bombs >= 2:
                self.fail = True
        else:
            hit_matrix[row][col] = 'hit'
            ship_id = ship_matrix[row][col]
            if self.check_sink(hit_matrix, ship_matrix, ship_id):
                self.sink_ship(hit_matrix, ship_matrix, ship_id)

    def check_sink(self, hit_matrix, ship_matrix, ship_id):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ship_matrix[row][col] == ship_id and hit_matrix[row][col] != 'hit':
                    return False
        return True

    def sink_ship(self, hit_matrix, ship_matrix, ship_id):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ship_matrix[row][col] == ship_id:
                    hit_matrix[row][col] = 'sunk'
        self.alive_ship -= 1


def main():
    battle = Battleship()
    ship_matrix = battle.random_ships()
    hit_matrix = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = battle.get_cell_pos(mouse_pos)
                if hit_matrix[row][col] == '':  # Only process clicks on unrevealed cells
                    battle.handle_click(hit_matrix, ship_matrix, row, col)

        screen.fill(BLUE)
        battle.draw_grid(hit_matrix, ship_matrix)
        pygame.display.flip()
        clock.tick(FPS)

        if battle.alive_ship == 0:
            print("You have won")
            running = False
        if battle.fail:
            print("RIDIIII")
            running = False


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
