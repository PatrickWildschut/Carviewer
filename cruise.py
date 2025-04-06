import pygame
import sys
import time
from Carviewer_global import *

# Variables
cruise_control_enabled = False
current_speed = 0  # The current speed of the vehicle
desired_speed = 0  # The speed set for cruise control
last_update_time = time.time()

def cruise_control_screen():
    global cruise_control_enabled, current_speed, desired_speed, last_update_time

    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = time.time()
        elapsed_time = current_time - last_update_time  # Time elapsed in seconds
        last_update_time = current_time

        # If cruise control is enabled, update the current speed to the desired speed
        if cruise_control_enabled:
            current_speed = desired_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check if enable/disable cruise control button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 150) <= y <= (HEIGHT - 100):
                    cruise_control_enabled = not cruise_control_enabled  # Toggle cruise control

                # Check if increase speed by 1 button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 50) <= y <= (HEIGHT) :
                    if not cruise_control_enabled:  # If cruise control is not enabled, adjust speed manually
                        current_speed += 1

                # Check if decrease speed by 1 button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    if not cruise_control_enabled:  # If cruise control is not enabled, adjust speed manually
                        current_speed -= 1

                # Check if increase speed by 5 button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 200) <= y <= (HEIGHT - 150):
                    if not cruise_control_enabled:  # If cruise control is not enabled, adjust speed manually
                        current_speed += 5

                # Check if decrease speed by 5 button is clicked
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 250) <= y <= (HEIGHT - 200):
                    if not cruise_control_enabled:  # If cruise control is not enabled, adjust speed manually
                        current_speed -= 5

                # Check if back button is clicked
                if 50 <= x <= 250 and 500 <= y <= 550:
                    return  # Exit function

        # Draw background
        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Display Current Speed and Desired Speed next to each other
        current_speed_text = font_large.render(f"{current_speed} km/h", True, TEXT_COLOR)
        desired_speed_text = font_large.render(f"Desired: {desired_speed} km/h", True, TEXT_COLOR)

        # Place them side by side
        screen.blit(current_speed_text, (WIDTH // 4 - 50, 200))
        screen.blit(desired_speed_text, (WIDTH // 2 + 50, 200))

        # Display Cruise Control Status
        cruise_control_status_text = font_large.render("Cruise Control: ON" if cruise_control_enabled else "Cruise Control: OFF", True, TEXT_COLOR)
        screen.blit(cruise_control_status_text, (WIDTH // 2 - 150, 300))

        # Enable/Disable Cruise Control Button (above speed controls)
        cruise_control_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, cruise_control_rect)
        cruise_control_text = font_small.render("Disable Cruise" if cruise_control_enabled else "Enable Cruise", True, BUTTON_TEXT_COLOR)
        text_rect = cruise_control_text.get_rect(center=cruise_control_rect.center)
        screen.blit(cruise_control_text, text_rect)

        # Speed Adjust Buttons (Horizontally centered in the bottom)
        button_width = 90
        button_height = 50
        button_spacing = 20
        base_y = HEIGHT - 100

        # Create Speed +5 button
        increase_5_rect = pygame.Rect(WIDTH // 2 - 2 * (button_width + button_spacing), base_y, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, increase_5_rect)
        increase_5_text = font_small.render("Speed +5", True, BUTTON_TEXT_COLOR)
        text_rect = increase_5_text.get_rect(center=increase_5_rect.center)
        screen.blit(increase_5_text, text_rect)

        # Create Speed +1 button
        increase_1_rect = pygame.Rect(WIDTH // 2 - (button_width + button_spacing), base_y, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, increase_1_rect)
        increase_1_text = font_small.render("Speed +1", True, BUTTON_TEXT_COLOR)
        text_rect = increase_1_text.get_rect(center=increase_1_rect.center)
        screen.blit(increase_1_text, text_rect)

        # Create Speed -1 button
        decrease_1_rect = pygame.Rect(WIDTH // 2 + button_spacing, base_y, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, decrease_1_rect)
        decrease_1_text = font_small.render("Speed -1", True, BUTTON_TEXT_COLOR)
        text_rect = decrease_1_text.get_rect(center=decrease_1_rect.center)
        screen.blit(decrease_1_text, text_rect)

        # Create Speed -5 button
        decrease_5_rect = pygame.Rect(WIDTH // 2 + 2 * (button_width + button_spacing), base_y, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, decrease_5_rect)
        decrease_5_text = font_small.render("Speed -5", True, BUTTON_TEXT_COLOR)
        text_rect = decrease_5_text.get_rect(center=decrease_5_rect.center)
        screen.blit(decrease_5_text, text_rect)

        # Back Button (Bottom Left)
        back_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, text_rect)

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    cruise_control_screen()
