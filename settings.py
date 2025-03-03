import pygame
import sys
import json

pygame.init()  # Initialize Pygame
from Carviewer_global import *


def get_json_fps():
    # read json
    with open("settings.json", "r") as file:
        settings_json = json.load(file)

    return settings_json["Program"]["fps"]

def settings_menu():
    running = True
    fps_options = [20, 30, 40, 50, 60]
    selected_fps = get_json_fps()

    clock = pygame.time.Clock()  # Initialize clock

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                speed_from_gpio.cancel()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= event.pos[0] <= 924 and 250 <= event.pos[1] <= 350:
                    selected_fps = fps_options[(event.pos[0] - 100) // 165]
                    update_json(selected_fps)
                # Check if back button is clicked
                elif 50 <= event.pos[0] <= 50 + 200 and 500 <= event.pos[1] <= 500 + 50:
                    return  # Return to main.py

        screen.fill(BACKGROUND_COLOR)
        title_text = font_large.render("Settings", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Draw back button
        back_button_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, text_rect)

        pygame.draw.rect(screen, BUTTON_COLOR, (100, 250, 824, 100))
        for i, fps in enumerate(fps_options):
            pygame.draw.rect(screen, BUTTON_COLOR, (100 + i * 165, 250, 150, 100))
            fps_text = font_small.render(f"{fps} FPS", True, BUTTON_TEXT_COLOR)
            screen.blit(fps_text, (100 + i * 165 + 75 - fps_text.get_width() // 2, 300 - fps_text.get_height() // 2))
            if fps == selected_fps:
                pygame.draw.rect(screen, (0, 255, 0), (100 + i * 165, 250, 150, 100), 3)

        pygame.display.flip()
        clock.tick(selected_fps)  # Limit frame rate

def update_json(fps):
    with open("settings.json", "r") as file:
        settings_data = json.load(file)

    settings_data["Program"]["fps"] = fps

    with open("settings.json", "w") as file:
        json.dump(settings_data, file, indent=4)
