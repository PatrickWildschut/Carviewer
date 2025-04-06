import pygame
import sys
import misc
import cruise
import settings
import subprocess

from Carviewer_global import *

settings_json = None

def read_menu():
    global settings_json

    settings_json = load_json()
    
    clock = pygame.time.Clock()
    running = True

    if len(sys.argv) > 1:
        if sys.argv[1] == "fullscreen":
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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

        # Update dashboard
        draw_dashboard(GetThrottlePercentage(), int(GetSpeed()), 
                       GetClutch(), GetBrake())

        if GetButtonPressed():
            cruise.cruise_control_screen()
        
        clock.tick(settings_json["Program"]["fps"])  # Limit frame rate
        
    pygame.quit()


# Function to draw dashboard
def draw_dashboard(throttle, speed, clutch_pressed, brake_pressed):
    screen.fill(BACKGROUND_COLOR)
    
    # Title
    title_text = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_text, (50, 50))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # version label
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, 550))
    
    # Throttle
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (50, 150))
    # pygame.draw.rect(screen, BUTTON_COLOR, (250, 150, throttle * 2, 30))

    throttle_circle_radius = 100
    pygame.draw.circle(screen, TEXT_COLOR, (300, 200), throttle_circle_radius, 3)
    pygame.draw.arc(screen, TEXT_COLOR, (200, 100, 200, 200), 3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)


    throttle_text = font_large.render(str(throttle), True, TEXT_COLOR)
    screen.blit(throttle_text, (300 - throttle_text.get_width() / 2, 200 - throttle_text.get_height() / 2))
    percent_text = font_small.render("%", True, TEXT_COLOR)
    screen.blit(percent_text, (325, 190))
    
    # Speed
    speed_label = font_small.render("Speed", True, TEXT_COLOR)
    screen.blit(speed_label, (550, 150))
    
    # Draw speed circle
    speed_circle_radius = 100
    pygame.draw.circle(screen, TEXT_COLOR, (800, 200), speed_circle_radius, 3)
    

    speed_text = None

    if speed > 105:
        speed_text = font_large.render(str(speed), True, RED)
        pygame.draw.arc(screen, RED, (700, 100, 200, 200), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
    else:
        speed_text = font_large.render(str(speed), True, TEXT_COLOR)
        pygame.draw.arc(screen, TEXT_COLOR, (700, 100, 200, 200), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
    
    screen.blit(speed_text, (800 - speed_text.get_width() / 2, 200 - speed_text.get_height() / 2))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (775, 225))
    
    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (50, 375))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (300, 375))
    
    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (550, 375))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (800, 375))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (50, 330), (950, 330), 2)
    pygame.draw.line(screen, TEXT_COLOR, (50, 450), (950, 450), 2)
    
    # Draw buttons
    button_width = 200
    button_height = 50
    
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)
    
    pygame.display.flip()

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
    #subprocess.Popen(['./Carplay.AppImage'])
    subprocess.run(["./Carplay.AppImage"])

# Function for Settings action
def settings_pressed():
    global settings_json

    settings.settings_menu()

    # update json, settings may have changed
    settings_json = load_json()

# Function for Misc action
def misc_pressed():
    misc.misc_screen()

