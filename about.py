import pygame
import sys
from Carviewer_global import *
import os
# # Initialize Pygame
# pygame.init()

# # Fonts
# font_large = pygame.font.Font(None, 48)
# font_small = pygame.font.Font(None, 36)

# # Colors
# BACKGROUND_COLOR = (30, 30, 30)
# TEXT_COLOR = (255, 255, 255)
# BUTTON_COLOR = (50, 50, 50)
# BUTTON_TEXT_COLOR = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)

# # Screen dimensions
# WIDTH, HEIGHT = 1024, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Carviewer 98-RS-RV")

def about_screen():
    running = True

    clock = pygame.time.Clock()  # Initialize clock

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # exit button
                if WIDTH - 200 <= event.pos[0] <= WIDTH - 50 and 50 <= event.pos[1] <= 50 + 30:
                    # stop pigpio
                    pi.stop()
                    os.system("sudo systemctl stop pigpiod &")
                    # turn off app
                    running = False
                elif WIDTH - 200 <= event.pos[0] <= WIDTH - 50 and HEIGHT - 80 <= event.pos[1] <= HEIGHT - 50:
                    pi.stop()
                    os.system("sudo systemctl stop pigpiod &")
                    os.system("shutdown now")
                # back button
                elif 50 <= event.pos[0] <= 50 + 200 and 500 <= event.pos[1] <= 500 + 50:
                    return  # Return to main.py

        screen.fill(BACKGROUND_COLOR)

        # About text
        about_text = font_large.render("About", True, TEXT_COLOR)
        screen.blit(about_text, (50, 50))

        # Draw back button
        back_button_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, text_rect)

        # Author
        author_text = font_small.render("Author: Patrick Wildschut", True, (240, 240, 240))  # Light gray color
        screen.blit(author_text, (50, 200))

        # Additional Text
        additional_text = font_small.render("Carviewer is a software application designed for the Ford Fiesta MK6 Sport.", True, (240, 240, 240))  # Light gray color
        screen.blit(additional_text, (50, 270))  # Increased spacing
        additional_text2 = font_small.render("It provides a dashboard-like interface for monitoring car parameters.", True, (240, 240, 240))  # Light gray color
        screen.blit(additional_text2, (50, 310))  # Increased spacing

        # Copyright
        copyright_text = font_small.render("© 2024-2025 Carviewer, All rights reserved.", True, (204, 204, 204))
        screen.blit(copyright_text, (50, 400))  # Increased spacing

        # Exit Button
        exit_button_rect = pygame.Rect(WIDTH - 200, 50, 150, 30)
        pygame.draw.rect(screen, BUTTON_COLOR, exit_button_rect)
        exit_text = font_small.render("Exit", True, BUTTON_TEXT_COLOR)
        text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, text_rect)

        # Shutdown Button
        shutdown_button_rect = pygame.Rect(WIDTH - 200, HEIGHT - 80, 150, 30)
        pygame.draw.rect(screen, BUTTON_COLOR, shutdown_button_rect)
        shutdown_text = font_small.render("Shutdown", True, BUTTON_TEXT_COLOR)
        text_rect = shutdown_text.get_rect(center=shutdown_button_rect.center)
        screen.blit(shutdown_text, text_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    about_screen()
