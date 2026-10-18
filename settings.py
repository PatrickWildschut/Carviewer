import pygame
import sys
import json
from Carviewer_Arduino import *

fps_options = [20, 30, 40, 50, 60]
layout_options = ["Original", "Fancy", "DiRT", "Modern"]

def get_json_settings():
    # read json
    with open("settings.json", "r") as file:
        settings_json = json.load(file)

    return settings_json["Program"]["layout"], settings_json["Program"]["fps"]

def settings_menu():
    running = True
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
                if S(100) <= event.pos[0] <= S(100) + len(layout_options) * S(206) and S(180) <= event.pos[1] <= S(280):
                    selected_layout = (event.pos[0] - S(100)) // S(206) # index of layout :)
                    update_json(selected_layout, selected_fps)
                    
                # FPS selection
                elif S(100) <= event.pos[0] <= S(100) + len(fps_options) * S(165) and S(360) <= event.pos[1] <= S(460):
                    selected_fps = fps_options[(event.pos[0] - S(100)) // S(165)]
                    update_json(selected_layout, selected_fps)
                # Back button
                elif S(50) <= event.pos[0] <= S(250) and S(500) <= event.pos[1] <= S(550):
                    return

        screen.fill(BACKGROUND_COLOR)
        title_text = font_large.render("Settings", True, TEXT_COLOR)
        screen.blit(title_text, (S(50), S(50)))

         # Layout section
        layout_title = font_small.render("Layout:", True, TEXT_COLOR)
        screen.blit(layout_title, (S(100), S(130)))

        pygame.draw.rect(screen, BUTTON_COLOR, (S(100), S(180), S(824), S(100)))
        for i, layout in enumerate(layout_options):
            rect_x = S(100) + i * S(206)
            pygame.draw.rect(screen, BUTTON_COLOR, (rect_x, S(180), S(200), S(100)))
            layout_text = font_small.render(layout, True, BUTTON_TEXT_COLOR)
            screen.blit(layout_text, (rect_x + S(100) - layout_text.get_width() // 2, S(230) - layout_text.get_height() // 2))
            if layout_options.index(layout) == selected_layout:
                pygame.draw.rect(screen, GREEN, (rect_x, S(180), S(200), S(100)), S(3))

        # FPS section
        fps_title = font_small.render("FPS:", True, TEXT_COLOR)
        screen.blit(fps_title, (S(100), S(330)))

        pygame.draw.rect(screen, BUTTON_COLOR, (S(100), S(360), S(824), S(100)))
        for i, fps in enumerate(fps_options):
            rect_x = S(100) + i * S(165)
            pygame.draw.rect(screen, BUTTON_COLOR, (rect_x, S(360), S(150), S(100)))
            fps_text = font_small.render(f"{fps} FPS", True, BUTTON_TEXT_COLOR)
            screen.blit(fps_text, (rect_x + S(75) - fps_text.get_width() // 2, S(410) - fps_text.get_height() // 2))
            if fps == selected_fps:
                pygame.draw.rect(screen, GREEN, (rect_x, S(360), S(150), S(100)), S(3))

        # Back button
        back_button_rect = pygame.Rect(S(50), S(500), S(200), S(50))
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

        pygame.display.flip()
        clock.tick(selected_fps)


def update_json(layout, fps):
    global layout_options

    with open("settings.json", "r") as file:
        settings_data = json.load(file)

    settings_data["Program"]["layout"] = layout
    settings_data["Program"]["fps"] = fps

    with open("settings.json", "w") as file:
        json.dump(settings_data, file, indent=4)
