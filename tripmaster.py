import pygame
import sys
import time
from Carviewer_global import *

# Variables
running_trip = False
trip_distance = 0.0
total_distance = 1200.0  # Assume 1200 km as total distance (can be loaded from a file)
last_update_time = time.time()

def tripmaster_screen():
    global running_trip, trip_distance, total_distance, last_update_time
    
    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = time.time()
        elapsed_time = current_time - last_update_time  # Time elapsed in seconds
        last_update_time = current_time

        # If trip is running, update distance
        if running_trip:

            current_speed = GetSpeed()

            trip_distance += (current_speed * (elapsed_time / 3600))  # Convert speed to km/s
            total_distance += (current_speed * (elapsed_time / 3600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check if reset trip button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    trip_distance = 0.0  # Reset trip distance
                
                # Check if start/stop button is clicked
                if (WIDTH - 250) <= x <= (WIDTH - 50) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    running_trip = not running_trip  # Toggle trip tracking
                
                # Check if back button is clicked
                if 50 <= x <= 250 and 500 <= y <= 550:
                    return  # Exit function

        # Draw background
        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Trip Master", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Display Current Trip Distance on the left
        trip_distance_text = font_large.render(f"{trip_distance:.2f} km", True, TEXT_COLOR)
        screen.blit(trip_distance_text, (100, 200))
        trip_label = font_small.render("Current Distance", True, TEXT_COLOR)
        screen.blit(trip_label, (100, 250))

        # Display Total Distance on the right
        total_distance_text = font_large.render(f"{total_distance:.2f} km", True, TEXT_COLOR)
        screen.blit(total_distance_text, (WIDTH - 250, 200))
        total_label = font_small.render("Total Distance", True, TEXT_COLOR)
        screen.blit(total_label, (WIDTH - 250, 250))

        # Reset Trip Button (center bottom)
        reset_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, reset_button_rect)
        reset_text = font_small.render("Reset Trip", True, BUTTON_TEXT_COLOR)
        text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, text_rect)
        
        # Start/Stop Trip Button (bottom right)
        start_stop_rect = pygame.Rect(WIDTH - 250, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, start_stop_rect)
        start_stop_text = font_small.render("Stop Trip" if running_trip else "Start Trip", True, BUTTON_TEXT_COLOR)
        text_rect = start_stop_text.get_rect(center=start_stop_rect.center)
        screen.blit(start_stop_text, text_rect)
        
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
    tripmaster_screen()
