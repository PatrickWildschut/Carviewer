import pygame
import sys

from Carviewer_global import *

import about
import stage
import tripmaster
import rev

def misc_screen():
    running = True
    clock = pygame.time.Clock()

    button_width, button_height = 250, 60
    button_spacing = 20
    start_y = HEIGHT // 2 - (3 * button_height + 2 * button_spacing) // 2

    buttons = {
        "Trip Master": pygame.Rect(WIDTH // 2 - button_width // 2, start_y, button_width, button_height),
        "Stage": pygame.Rect(WIDTH // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height),
        "Revving": pygame.Rect(WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height),
        "About": pygame.Rect(WIDTH - 150, 50, 100, 30),
        "Back": pygame.Rect(50, 500, 200, 50)
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if buttons["Back"].collidepoint(x, y):
                    return  # Return to main.py
                elif buttons["About"].collidepoint(x, y):
                    about.about_screen()
                elif buttons["Trip Master"].collidepoint(x, y):
                    tripmaster.tripmaster_screen()
                elif buttons["Stage"].collidepoint(x, y):
                    stage.stage_screen()
                elif buttons["Revving"].collidepoint(x, y):
                    rev.revving_screen()

        screen.fill(BACKGROUND_COLOR)

        # Draw buttons
        for label, rect in buttons.items():
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            button_text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    misc_screen()