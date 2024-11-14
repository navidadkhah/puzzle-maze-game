from colors import WHITE, BLACK, RED
import pygame


def impossible_maze():
    print("hereee")
    # Define mini-maze settings
    mini_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    mini_cell_size = 20
    mini_player_pos = [5, 0]

    # Create a new window for the mini maze
    new_screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("Mini Maze Game")

    def draw_mini_maze():
        for row in range(13):
            for col in range(13):
                color = BLACK if mini_maze[row][col] == 1 else WHITE
                pygame.draw.rect(new_screen, color,
                                 (col * mini_cell_size, row * mini_cell_size, mini_cell_size, mini_cell_size))
        pygame.draw.rect(new_screen, RED, (
            mini_player_pos[1] * mini_cell_size, mini_player_pos[0] * mini_cell_size, mini_cell_size, mini_cell_size))

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

        if mini_player_pos == [5, 12]:
            waiting_for_key = False
            print("You solved the puzzle!!!")
            score = 60
            state = True

    # Reset to original screen size
    pygame.display.set_mode((23 * 20, 23 * 20))
    return score, state
