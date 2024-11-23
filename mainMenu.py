import pygame
import sys
from colors import WHITE, BLACK, GREEN, RED, LIGHT_BLUE
from main import play_game

pygame.init()

cell_size = 20  # Size of each cell in the grid
grid_size = 23  # Size of the maze (23x23)

screen_size = grid_size * cell_size
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Freaky Puzzle")

# Load and scale the background image to fit the screen size
background_image = pygame.image.load('Images/menu.png')
background_image = pygame.transform.scale(background_image,
                                          (screen_size, screen_size))  # Scale the image to fill the screen


def draw_button(screen, text, x, y, width, height, base_color, text_color, border_radius=10):
    # Gradient effect
    gradient_color = [(base_color[i] + (255 - base_color[i]) // 2) for i in range(3)]
    for i in range(height):
        color = [(base_color[j] * (height - i) // height + gradient_color[j] * i // height) for j in range(3)]
        pygame.draw.rect(screen, color, (x, y + i, width, 1),
                         border_radius=border_radius if i == 0 or i == height - 1 else 0)

    # Adding text to button
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def main_menu():
    running = True
    note = ""
    level = ""
    score = ""
    while running:
        # Display the background image
        screen.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 48)
        details_font = pygame.font.Font(None, 24)

        title_text = font.render('Freaky Puzzle', True, BLACK)
        note_text = details_font.render(f'{note}', True, BLACK)  # Display notes from play_game
        if level:
          score_text = details_font.render(f'Score: {score}', True, BLACK)  # Display notes from play_game
          level_text = details_font.render(f'Level: {level}', True, BLACK)  # Display level from play_game
          note_rect = note_text.get_rect(center=(screen_size // 2, screen_size // 3.25))
          score_rect = score_text.get_rect(center=(screen_size // 2, screen_size // 2.75))
          level_rect = level_text.get_rect(center=(screen_size // 2, screen_size // 2.5))
          screen.blit(note_text, note_rect)
          screen.blit(level_text, level_rect)
          screen.blit(score_text, score_rect)


        title_rect = title_text.get_rect(center=(screen_size // 2, screen_size // 5))


        screen.blit(title_text, title_rect)


        draw_button(screen, 'Play', screen_size // 4, screen_size // 2, screen_size // 2, 50, GREEN, BLACK)
        draw_button(screen, 'Instructions', screen_size // 4, screen_size // 2 + 80, screen_size // 2, 50, RED, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_size // 4 <= mouse_x <= screen_size * 3 // 4 and screen_size // 2 <= mouse_y <= screen_size // 2 + 30:
                    note, level, score = play_game()  # Start the game and capture results
                elif screen_size // 4 <= mouse_x <= screen_size * 3 // 4 and screen_size // 2 + 80 <= mouse_y <= screen_size // 2 + 110:
                    show_instructions()  # Show instructions


def show_instructions():
    # Create a new Pygame window for instructions
    instructions_running = True
    instructions_screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Instructions")

    # Define the font and text for the instructions
    font = pygame.font.Font(None, 20)
    title_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Game Instructions", True, BLACK)
    instructions_text = [
        "1. Navigate through the maze to reach the goal.",
        "2. Use arrow keys to move your character.",
        "3. Each gray obstacles has a game, win them to open your way.",
        "4. You have limited lives, so play carefully.",
        "5. Completing the puzzle gives a bonus score.",
        "6. Some portals and teleports are in the game, use them.",
    ]

    # Main loop for the instructions screen
    while instructions_running:
        instructions_screen.fill(LIGHT_BLUE)

        # Draw the title
        title_rect = title_text.get_rect(center=(screen_size // 2, 50))
        instructions_screen.blit(title_text, title_rect)

        # Draw the instructions text
        for i, line in enumerate(instructions_text):
            line_surface = font.render(line, True, BLACK)
            line_rect = line_surface.get_rect(topleft=(50, 100 + i * 30))
            instructions_screen.blit(line_surface, line_rect)

        # Draw the Back button
        draw_button(instructions_screen, "Back", screen_size // 4, screen_size - 100, screen_size // 2, 50, RED, BLACK)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_size // 4 <= mouse_x <= screen_size * 3 // 4 and screen_size - 100 <= mouse_y <= screen_size - 50:
                    instructions_running = False  # Exit the instructions screen

