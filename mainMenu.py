import pygame
import sys
from colors import WHITE, BLACK, GREEN, RED
from main import play_game



# Initialize Pygame
pygame.init()

# # Set up display
screen_size = 460  # Adjusted screen size for better viewing
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Freaky Puzzle")
#

#
#
def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def main_menu():
    print("here")
    running = True
    while running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 48)
        title_text = font.render('Freaky Puzzle', True, BLACK)
        title_rect = title_text.get_rect(center=(screen_size // 2, screen_size // 5))

        screen.blit(title_text, title_rect)
        draw_button(screen, 'Play', screen_size // 4, screen_size // 2 - 20, screen_size // 2, 50, GREEN, BLACK)
        draw_button(screen, 'Instructions', screen_size // 4, screen_size // 2 + 60, screen_size // 2, 50, RED, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_size // 4 <= mouse_x <= screen_size * 3 // 4 and screen_size // 2 - 20 <= mouse_y <= screen_size // 2 + 30:
                    play_game()  # Start the game
                elif screen_size // 4 <= mouse_x <= screen_size * 3 // 4 and screen_size // 2 + 60 <= mouse_y <= screen_size // 2 + 110:
                    show_instructions()  # Show instructions

    pygame.quit()
    sys.exit()

def show_instructions():
    # Placeholder for the instructions display
    print("Instructions")
