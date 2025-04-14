import pygame
import sys
import time
from Carviewer_global import *

revving_percent = 0

def revving_screen():
    global revving_percent
    running = True
    clock = pygame.time.Clock()
    
    slider_x = 200
    slider_y = 400
    slider_width = 600
    slider_height = 20

    dragging = False
    revving = False
    countdown_start_time = None  # Timestamp for countdown

    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 50 <= event.pos[0] <= 250 and 500 <= event.pos[1] <= 550:
                    return

                if WIDTH//2 - 150 <= event.pos[0] <= WIDTH//2 + 150 and 250 <= event.pos[1] <= 310:
                    revving = not revving
                    if revving:
                        countdown_start_time = time.time()
                    else:
                        countdown_start_time = None  # Reset countdown

                if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_height:
                    dragging = True
                    revving = False
                    countdown_start_time = None

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                relative_x = min(max(event.pos[0], slider_x), slider_x + slider_width)
                revving_percent = int(((relative_x - slider_x) / slider_width) * 100)
                revving = False
                countdown_start_time = None

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Revving", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Handle countdown
        if revving:
            if countdown_start_time:
                time_passed = current_time - countdown_start_time
                countdown = max(0, 5 - int(time_passed))
                countdown_text = font_large.render(f"{countdown}", True, (255, 100, 100))
                screen.blit(countdown_text, (WIDTH//2 - 15, 180))

                if time_passed >= 5:
                    revving_action()
                    countdown_start_time = time.time()  # Restart countdown

        SetRelays(revving)

        # Start/Stop Revving Button
        button_label = "Stop Revving" if revving else "Start Revving"
        rev_button_rect = pygame.Rect(WIDTH//2 - 150, 250, 300, 60)
        pygame.draw.rect(screen, BUTTON_COLOR, rev_button_rect)
        rev_text = font_small.render(button_label, True, BUTTON_TEXT_COLOR)
        rev_text_rect = rev_text.get_rect(center=rev_button_rect.center)
        screen.blit(rev_text, rev_text_rect)

        # Slider
        pygame.draw.rect(screen, SLIDER_COLOR, (slider_x, slider_y, slider_width, slider_height))
        fill_width = int((revving_percent / 100) * slider_width)
        pygame.draw.rect(screen, SLIDER_FILL_COLOR, (slider_x, slider_y, fill_width, slider_height))
        percent_text = font_small.render(f"{revving_percent}%", True, TEXT_COLOR)
        screen.blit(percent_text, (slider_x + slider_width + 10, slider_y - 5))

        # Back Button
        back_button_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def revving_action():
    SetThrottle(2*revving_percent/100)
    pygame.time.delay(100)
    SetThrottle(0)

if __name__ == "__main__":
    revving_screen()
