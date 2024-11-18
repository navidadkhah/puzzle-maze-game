import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display

def text_puzzle_question(screen, question):
    farsi_font = pygame.font.Font("./YekanBakh-VF.ttf", 15)

    input_box = pygame.Rect(100, 200, 400, 50)
    color = pygame.Color('white')
    active = False
    text = ''

    clock = pygame.time.Clock()
    done = False

    # Reshape and reorder the question for proper Farsi rendering
    reshaped_question = arabic_reshaper.reshape(question)
    bidi_question = get_display(reshaped_question)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Submit the answer
                    return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # Fill the screen with a dark background
        screen.fill((30, 30, 30))  # Background color

        # Render the reshaped question text
        question_surface = farsi_font.render(bidi_question, True, pygame.Color('white'))
        screen.blit(question_surface, (100, 150))

        # Reshape and reorder the input text for proper Farsi rendering
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        # Render the input text
        txt_surface = farsi_font.render(bidi_text, True, pygame.Color('white'))  # Set to white
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)  # Draw the input box border

        pygame.display.flip()
        clock.tick(30)