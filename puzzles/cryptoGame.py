import pygame
import random

def play_cipher_game():
    """Launch the cipher game and return the score."""
    pygame.init()
    
    # Screen Dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cipher Game")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (100, 100, 255)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)

    # Fonts
    FONT = pygame.font.Font(None, 36)

    # Game Variables
    plaintext = "HELLO WORLD"
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    cipher_map = {plain: cipher for plain, cipher in zip(alphabet, shuffled)}
    cipher_text = "".join(cipher_map[char] if char.isalpha() else char for char in plaintext)

    revealed_letters = random.sample([char for char in plaintext if char.isalpha()], 2)
    guessed_letters = {cipher_map[char]: char for char in revealed_letters}
    keyboard = {chr(65 + i): False for i in range(26)}
    for char in guessed_letters.values():
        keyboard[char] = True

    selected_block = None

    def draw_text(surface, text, x, y, color):
        label = FONT.render(text, True, color)
        surface.blit(label, (x, y))

    def draw_blocks():
        """Draw the cipher blocks on the screen and highlight the selected one."""
        for i, char in enumerate(cipher_text):
            x = 50 + (i % (WIDTH // 50)) * 50
            y = 50 + (i // (WIDTH // 50)) * 50
            
            # Highlight selected block with blue border
            if selected_block == char:
                pygame.draw.rect(screen, BLUE, (x, y, 50, 50))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, 50, 50))
            
            pygame.draw.rect(screen, BLACK, (x, y, 50, 50), 2)  # Outline

            # Display guessed letter, revealed letter, or cipher letter
            if char in guessed_letters:
                draw_text(screen, guessed_letters[char], x + 15, y + 10, GREEN)
            elif char in cipher_map and cipher_map[char] in revealed_letters:
                draw_text(screen, cipher_map[char], x + 15, y + 10, BLUE)
            else:
                draw_text(screen, char, x + 15, y + 10, RED)


    def draw_keyboard():
        for i, key in enumerate(keyboard):
            x = 50 + (i % 10) * 50
            y = HEIGHT - 150 + (i // 10) * 50
            pygame.draw.rect(screen, WHITE if not keyboard[key] else GREEN, (x, y, 50, 50))
            pygame.draw.rect(screen, BLACK, (x, y, 50, 50), 2)
            draw_text(screen, key, x + 15, y + 10, BLACK if not keyboard[key] else WHITE)

    running = True
    while running:
        screen.fill(WHITE)
        draw_blocks()
        draw_keyboard()
        draw_text(screen, "Guess the message!", 50, 10, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 50 <= my < HEIGHT - 200:
                    row = (my - 50) // 50
                    col = (mx - 50) // 50
                    index = row * (WIDTH // 50) + col
                    if 0 <= index < len(cipher_text):
                        selected_block = cipher_text[index]
                elif HEIGHT - 200 <= my:
                    row = (my - (HEIGHT - 150)) // 50
                    col = (mx - 50) // 50
                    index = row * 10 + col
                    if 0 <= index < 26:
                        selected_char = chr(65 + index)
                        if selected_block and not keyboard[selected_char]:
                            if selected_block in guessed_letters:
                                previous_guess = guessed_letters[selected_block]
                                keyboard[previous_guess] = False
                            guessed_letters[selected_block] = selected_char
                            keyboard[selected_char] = True

        current_guess = "".join(guessed_letters.get(char, char) for char in cipher_text)
        if current_guess.replace(" ", "") == plaintext.replace(" ", ""):
            score = sum(
                1 for char in plaintext if char.isalpha() and guessed_letters.get(cipher_map[char], "") == char
            )
            return score, True

        pygame.display.flip()
