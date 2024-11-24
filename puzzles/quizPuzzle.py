import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display


def wrap_text(text, font, max_width):
    """Wrap text into multiple lines based on the available width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width - 300:  # Check if the line fits
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:  # Append any remaining text
        lines.append(current_line)

    lines.reverse()

    return lines


def text_puzzle_question(screen, question, image_path=None):
    pygame.init()

    farsi_font = pygame.font.Font("./assets/fonts/YekanBakh-VF.ttf", 12)

    input_box = pygame.Rect(50, 100, 400, 50)  # Adjust position for input box
    if image_path:
        # Push input box down if there's an image
        input_box = pygame.Rect(50, 350, 400, 50)

    color = pygame.Color('white')
    active = False
    text = ''

    clock = pygame.time.Clock()
    done = False

    # Reshape and reorder the question for proper Farsi rendering
    reshaped_question = arabic_reshaper.reshape(question)
    bidi_question = get_display(reshaped_question)

    # Wrap the reshaped question into multiple lines
    max_width = 700  # Adjust as needed based on your screen width
    wrapped_question_lines = wrap_text(bidi_question, farsi_font, max_width)

    # Load the image if provided
    image = None
    if image_path:
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(
                image, (300, 200))  # Scale the image to fit
        except pygame.error as e:
            print(f"Unable to load image: {e}")
            image = None

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

        # Render the wrapped question text
        y_offset = 50
        for line in wrapped_question_lines:
            question_surface = farsi_font.render(
                line, True, pygame.Color('white'))
            screen.blit(question_surface, (50, y_offset))
            y_offset += farsi_font.get_linesize()  # Move down for the next line

        # Display the image if loaded
        if image:
            screen.blit(image, (50, y_offset))
            y_offset += 220  # Move input box below the image

        # Reshape and reorder the input text for proper Farsi rendering
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        # Render the input text
        txt_surface = farsi_font.render(
            bidi_text, True, pygame.Color('white'))  # Set to white
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        input_box.y = y_offset + 10  # Adjust input box position dynamically
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Draw the input box border
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
