import pygame
import sys
import misc
import cruise
import settings
import subprocess
import layouts

from Carviewer_global import *

settings_json = None

def read_menu():
    global settings_json

    settings_json = load_json()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the Apple Carplay button area
                if 50 <= event.pos[0] <= 50 + 200 and 500 <= event.pos[1] <= 500 + 50:
                    apple_carplay()
                # Check if the mouse click is within the Settings button area
                elif WIDTH - 50 - 200 <= event.pos[0] <= WIDTH - 50 and 500 <= event.pos[1] <= 500 + 50:
                    settings_pressed()
                # Check if the mouse click is within the Misc button area
                elif WIDTH - 150 <= event.pos[0] <= WIDTH - 50 and 50 <= event.pos[1] <= 50 + 30:
                    misc_pressed()

        selected_layout = settings_json["Program"]["layout"]

        if selected_layout == "Original":
            layouts.original_dashboard(GetThrottlePercentage(), GetSpeed(), GetRPM(), 
                       GetClutch(), GetBrake(), GetGear())
        elif selected_layout == "Fancy":
            layouts.fancy_dashboard(GetThrottlePercentage(), GetSpeed(), GetRPM(), 
                       GetClutch(), GetBrake(), GetGear())
        elif selected_layout == "DiRT":
            layouts.dirt_dashboard(GetThrottlePercentage(), GetSpeed(), GetRPM(), 
                       GetClutch(), GetBrake(), GetGear())
        elif selected_layout == "F1":
            layouts.modern_dashboard(GetThrottlePercentage(), GetSpeed(), GetRPM(), 
                       GetClutch(), GetBrake(), GetGear())   

        pygame.display.flip()

        if GetButtonPressed():
            cruise.cruise_control_screen(None)
        
        clock.tick(settings_json["Program"]["fps"])  # Limit frame rate
        
    pygame.quit()
    
    

def fade_effect():
    font_oac = pygame.font.Font(None, 64)
    OVERLAY_COLOR = (30, 30, 30, 180)
    fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha = 0

    while alpha < 180:  # Fade in effect
        fade_surface.fill((30, 30, 30, alpha))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)
        alpha += 10

    # Display the "Opening Apple CarPlay" message
    fade_surface.fill(OVERLAY_COLOR)
    screen.blit(fade_surface, (0, 0))
    
    carplay_text = font_oac.render("Opening Apple CarPlay", True, TEXT_COLOR)
    text_rect = carplay_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(carplay_text, text_rect)

    pygame.display.flip()

# Function for Apple Carplay action
def apple_carplay():
    fade_effect()
    carplay = subprocess.Popen(['./Carplay.AppImage'])
    time.sleep(5)
    cruise.cruise_control_screen(carplay)
    #subprocess.run(["./Carplay.AppImage"])

# Function for Settings action
def settings_pressed():
    global settings_json

    settings.settings_menu()

    # update json, settings may have changed
    settings_json = load_json()

# Function for Misc action
def misc_pressed():
    misc.misc_screen()

if __name__ == "__main__":
    read_menu()