from assets.colors import WHITE, BLACK, RED
import pygame


def impossible_maze():
    print("hereee")
    # Define mini-maze settings
    mini_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    mini_cell_size = 20
    mini_grid_size = 14  # Size of the maze (9x9)

    mini_screen_size = mini_grid_size * mini_cell_size
    new_screen = pygame.display.set_mode((mini_screen_size, mini_screen_size))

    arrow_image = pygame.image.load('../Images/Arrow.jpg')
    arrow_image = pygame.transform.scale(arrow_image, (mini_cell_size, mini_cell_size))  # Scale it to fit the cell

    pygame.display.set_caption("Mini Maze Game")
    mini_player_pos = [5, 0]


    def draw_mini_maze():
        for row in range(mini_grid_size):
            for col in range(mini_grid_size + 1):
                color = BLACK if mini_maze[row][col] == 1 else WHITE
                pygame.draw.rect(new_screen, color,
                                 (col * mini_cell_size, row * mini_cell_size, mini_cell_size, mini_cell_size))
        center_x = mini_player_pos[1] * mini_cell_size + mini_cell_size // 2
        center_y = mini_player_pos[0] * mini_cell_size + mini_cell_size // 2
        pygame.draw.circle(new_screen, RED, (center_x, center_y), mini_cell_size // 2)
        new_screen.blit(arrow_image, (0 * mini_cell_size, 5 * mini_cell_size))
        new_screen.blit(arrow_image, (13 * mini_cell_size, 5 * mini_cell_size))


    draw_mini_maze()
    pygame.display.flip()

    # Event loop for the mini maze
    waiting_for_key = True
    score = 0
    state = False
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_key = False  # Close mini-game on 'escape' key
                    score = -10
                    state = False
                # Movement keys for the mini-game
                elif event.key == pygame.K_UP and mini_maze[mini_player_pos[0] - 1][mini_player_pos[1]] == 0:
                    mini_player_pos[0] -= 1
                elif event.key == pygame.K_DOWN and mini_maze[mini_player_pos[0] + 1][mini_player_pos[1]] == 0:
                    mini_player_pos[0] += 1
                elif event.key == pygame.K_LEFT and mini_maze[mini_player_pos[0]][mini_player_pos[1] - 1] == 0:
                    mini_player_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and mini_maze[mini_player_pos[0]][mini_player_pos[1] + 1] == 0:
                    mini_player_pos[1] += 1
                draw_mini_maze()
                pygame.display.flip()

        if mini_player_pos == [5, 13]:
            waiting_for_key = False
            print("You solved the puzzle!!!")
            score = 60
            state = True

    # Reset to original screen size
    pygame.display.set_mode((23 * 20, 23 * 20))
    return score, state
