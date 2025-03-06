import pygame
import sys
import time
from Carviewer_global import *

stage_running = False
waiting_for_start = False
start_time = 0
elapsed_time = 0
total_distance = 0

def format_time(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

def stage_screen():
    global stage_running, waiting_for_start, start_time, elapsed_time, total_distance

    running = True
    clock = pygame.time.Clock()
    
    ready_button_label = "Start"

    while running:
        current_time = time.time()
        current_speed = GetSpeed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check if Ready/Stop button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    if not stage_running and waiting_for_start:
                        ready_button_label = "Ready..."
                    elif stage_running:
                        stage_running = False  # Stop timing
                        elapsed_time = int((time.time() - start_time) * 1000)  # Convert to ms
                        ready_button_label = "Start"
                        waiting_for_start = False
                    else:
                        total_distance = 0.0  # Reset distance when ready is clicked again
                        elapsed_time = 0
                        ready_button_label = "Ready..."
                        waiting_for_start = True  # Waiting for movement
                        
                # Check if back button is clicked
                if 50 <= x <= 250 and 500 <= y <= 550:
                    return

        if waiting_for_start and current_speed > 0:
            ready_button_label = "Stop"
            stage_running = True
            start_time = time.time()
            total_distance = 0.0  # Reset distance counter
            waiting_for_start = False

        # If stage is running, update elapsed time and distance
        if stage_running:
            elapsed_time = int((time.time() - start_time) * 1000)  # Convert to ms
            total_distance += (current_speed * (clock.get_time() / 3600000))  # Distance in km

        # Draw background
        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Stage", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Labels
        time_label = font_small.render("Elapsed Time", True, TEXT_COLOR)
        distance_label = font_small.render("Total Distance", True, TEXT_COLOR)
        speed_label = font_small.render("Current Speed" if stage_running else "Average Speed", True, TEXT_COLOR)

        # Data
        time_text = font_large.render(format_time(elapsed_time), True, TEXT_COLOR)
        total_distance_text = font_large.render(f"{total_distance:.2f} km", True, TEXT_COLOR)
        
        if not stage_running:
            if elapsed_time > 0:
                avg_speed = (total_distance * 3600000) / elapsed_time  # Convert km/ms to km/h
                speed_text = font_large.render(f"{avg_speed:.2f} km/h", True, TEXT_COLOR)
            else:
                speed_text = font_large.render("0.00 km/h", True, TEXT_COLOR)
        else:
            speed_text = font_large.render(f"{current_speed:.2f} km/h", True, TEXT_COLOR)

        # Align everything nicely
        center_x = WIDTH // 2
        base_y = 150
        spacing = 80

        screen.blit(time_label, (center_x - time_label.get_width() // 2, base_y))
        screen.blit(time_text, (center_x - time_text.get_width() // 2, base_y + 30))

        screen.blit(distance_label, (center_x - distance_label.get_width() // 2, base_y + spacing))
        screen.blit(total_distance_text, (center_x - total_distance_text.get_width() // 2, base_y + spacing + 30))

        screen.blit(speed_label, (center_x - speed_label.get_width() // 2, base_y + 2 * spacing))
        screen.blit(speed_text, (center_x - speed_text.get_width() // 2, base_y + 2 * spacing + 30))

        # Ready/Stop Button (center bottom)
        ready_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, ready_button_rect)
        ready_text = font_small.render(ready_button_label, True, BUTTON_TEXT_COLOR)
        text_rect = ready_text.get_rect(center=ready_button_rect.center)
        screen.blit(ready_text, text_rect)

        # Back Button (Bottom Left, same size as in about)
        back_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, text_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    stage_screen()
