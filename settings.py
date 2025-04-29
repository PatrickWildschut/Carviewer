import pygame
import sys
import json
from Carviewer_global import *


def get_json_settings():
    # read json
    with open("settings.json", "r") as file:
        settings_json = json.load(file)

    return settings_json["Program"]["layout"], settings_json["Program"]["fps"]

def settings_menu():
    running = True
    fps_options = [20, 30, 40, 50, 60]
    layout_options = ["Original", "Fancy", "DiRT", "F1"]
    selected_layout, selected_fps = get_json_settings()

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Layout selection
                if 100 <= event.pos[0] <= 100 + len(layout_options) * 206 and 180 <= event.pos[1] <= 280:
                    selected_layout = layout_options[(event.pos[0] - 100) // 206]
                    update_json(selected_layout, selected_fps)
                    
                # FPS selection
                elif 100 <= event.pos[0] <= 100 + len(fps_options) * 165 and 360 <= event.pos[1] <= 460:
                    selected_fps = fps_options[(event.pos[0] - 100) // 165]
                    update_json(selected_layout, selected_fps)
                # Back button
                elif 50 <= event.pos[0] <= 250 and 500 <= event.pos[1] <= 550:
                    return

        screen.fill(BACKGROUND_COLOR)
        title_text = font_large.render("Settings", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

         # Layout section
        layout_title = font_small.render("Layout:", True, TEXT_COLOR)
        screen.blit(layout_title, (100, 130))

        pygame.draw.rect(screen, BUTTON_COLOR, (100, 180, 824, 100))
        for i, layout in enumerate(layout_options):
            rect_x = 100 + i * 206
            pygame.draw.rect(screen, BUTTON_COLOR, (rect_x, 180, 200, 100))
            layout_text = font_small.render(layout, True, BUTTON_TEXT_COLOR)
            screen.blit(layout_text, (rect_x + 100 - layout_text.get_width() // 2, 230 - layout_text.get_height() // 2))
            if layout == selected_layout:
                pygame.draw.rect(screen, GREEN, (rect_x, 180, 200, 100), 3)

        # FPS section
        fps_title = font_small.render("FPS:", True, TEXT_COLOR)
        screen.blit(fps_title, (100, 330))

        pygame.draw.rect(screen, BUTTON_COLOR, (100, 360, 824, 100))
        for i, fps in enumerate(fps_options):
            rect_x = 100 + i * 165
            pygame.draw.rect(screen, BUTTON_COLOR, (rect_x, 360, 150, 100))
            fps_text = font_small.render(f"{fps} FPS", True, BUTTON_TEXT_COLOR)
            screen.blit(fps_text, (rect_x + 75 - fps_text.get_width() // 2, 410 - fps_text.get_height() // 2))
            if fps == selected_fps:
                pygame.draw.rect(screen, GREEN, (rect_x, 360, 150, 100), 3)

        # Back button
        back_button_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

        pygame.display.flip()
        clock.tick(selected_fps)


def update_json(layout, fps):
    with open("settings.json", "r") as file:
        settings_data = json.load(file)

    settings_data["Program"]["layout"] = layout
    settings_data["Program"]["fps"] = fps

    with open("settings.json", "w") as file:
        json.dump(settings_data, file, indent=4)
