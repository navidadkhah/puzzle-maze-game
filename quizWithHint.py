import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display


def quiz_game_with_hint(screen, question, correct_answer, hints):
    pygame.init()
    
    # Initialize fonts and colors
    farsi_font = pygame.font.Font("./YekanBakh-VF.ttf", 15)
    color = pygame.Color('white')
    hint_color = pygame.Color('yellow')
    input_box = pygame.Rect(50, 300, 400, 50)

    text = ''
    score = 0
    wrong_attempts = 0
    max_attempts = 5

    done = False

    # Reshape and reorder the question and correct answer for proper Farsi rendering
    reshaped_question = arabic_reshaper.reshape(question)
    bidi_question = get_display(reshaped_question)

    # Reshape hints for Farsi rendering
    reshaped_hints = [get_display(arabic_reshaper.reshape(hint)) for hint in hints]

    hint_to_display = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check the answer
                    if text.strip() == correct_answer:
                        score += 5
                        return text.strip()
                    else:
                        wrong_attempts += 1
                        score -= 1

                        # Display hints based on the number of wrong attempts
                        if wrong_attempts == 2:
                            hint_to_display = reshaped_hints[0]
                        elif wrong_attempts == 4:
                            hint_to_display = reshaped_hints[1]

                        if wrong_attempts >= max_attempts:
                            return f"بازی تمام شد! امتیاز شما: {score}" if score > 0 else "شما باختید!"

                        text = ''  # Clear the input box after wrong answer
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # Fill the screen with a dark background
        screen.fill((30, 30, 30))  # Background color

        # Render the question text
        question_surface = farsi_font.render(bidi_question, True, color)
        screen.blit(question_surface, (50, 50))

        # Render hints if any
        if hint_to_display:
            hint_surface = farsi_font.render(hint_to_display, True, hint_color)
            screen.blit(hint_surface, (50, 200))

        # Render the input text
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        txt_surface = farsi_font.render(bidi_text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Render the current score
        score_text = f"امتیاز شما: {score}"
        reshaped_score_text = arabic_reshaper.reshape(score_text)
        bidi_score_text = get_display(reshaped_score_text)
        score_surface = farsi_font.render(bidi_score_text, True, color)
        screen.blit(score_surface, (50, 400))

        pygame.display.flip()