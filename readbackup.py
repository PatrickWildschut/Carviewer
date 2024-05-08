import pygame
import sys
import json
import about
import settings
import RPi.GPIO as GPIO
import subprocess
from ADCDACPi import ADCDACPi

from Carviewer_global import *

settings_json = None
open_carplay = False

def read_menu():
    global settings_json
    throttle = 50  # Throttle percentage
    speed = 60     # Speed in km/h

    settings_json = load_json()
    print(settings_json)
    
    clock = pygame.time.Clock()
    running = True
    open_carplay = False

    adc = ADCDACPi(1)

    adc.set_adc_refvoltage(3.3)
    
    # Set display mode to fullscreen
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
                # Check if the mouse click is within the About button area
                elif WIDTH - 150 <= event.pos[0] <= WIDTH - 50 and 50 <= event.pos[1] <= 50 + 30:
                    about_pressed()
        
        # Throttle
        throttle = adc.read_adc_voltage(1, 0) / 3.3 * 100

        # Speed
        speed += 1
        if speed > 200:
            speed = 0
        clutch_pressed = GPIO.input(settings_json["GPIO"]["clutch"])
        brake_pressed = GPIO.input(settings_json["GPIO"]["brake"])

        # Update dashboard
        draw_dashboard(throttle, speed, clutch_pressed, brake_pressed)
        
        clock.tick(settings_json["Program"]["fps"])  # Limit frame rate
        
    pygame.quit()


# Function to draw dashboard
def draw_dashboard(throttle, speed, clutch_pressed, brake_pressed):
    global open_carplay

    screen.fill(BACKGROUND_COLOR)
    
    # Title
    title_text = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_text, (50, 50))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    about_text = font_small.render("About", True, BUTTON_TEXT_COLOR)
    text_rect = about_text.get_rect(center=about_button_rect.center)
    screen.blit(about_text, text_rect)

    # Version label
    version_text = ''

    if open_carplay == True:
        version_text = font_small.render("Opening Apple Carplay...", True, TEXT_COLOR)
    else:
        version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, 550))
    
    # Throttle
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (50, 150))
    pygame.draw.rect(screen, BUTTON_COLOR, (250, 150, throttle * 2, 30))
    
    # Speed
    # speed_label = font_small.render("Speed", True, TEXT_COLOR)
    # screen.blit(speed_label, (550, 150))
    # if speed > 105:
    #     speed_text = font_small.render(f"{speed} km/h", True, (255, 0, 0))
    # else:
    #     speed_text = font_small.render(f"{speed} km/h", True, TEXT_COLOR)
    # screen.blit(speed_text, (800, 150))
    
    pygame.draw.circle(screen, TEXT_COLOR, (150, 150), 100, 3)
    pygame.draw.arc(screen, TEXT_COLOR, (75, 75, 150, 150), 3 * 3.14 / 4, 3 * 3.14 / 4 + speed * 3.14 / 200, 10)
    speed_text = font_large.render(str(speed), True, TEXT_COLOR)
    screen.blit(speed_text, (135 - speed_text.get_width() / 2, 140 - speed_text.get_height() / 2))
    pygame.draw.rect(screen, TEXT_COLOR, (130, 200, 40, 3))
    
    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (50, 300))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, (255, 0, 0) if clutch_pressed else (0, 255, 0))
    screen.blit(clutch_text, (300, 300))
    
    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (550, 300))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, (255, 0, 0) if brake_pressed else (0, 255, 0))
    screen.blit(brake_text, (800, 300))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (50, 200), (950, 200), 2)
    pygame.draw.line(screen, TEXT_COLOR, (50, 350), (950, 350), 2)
    
    # Draw buttons
    button_width = 200
    button_height = 50
    
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple Carplay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)
    
    pygame.display.flip()

# Function for Apple Carplay action
def apple_carplay():
    global open_carplay
    open_carplay = True
    carplay = subprocess.Popen(['./Carplay.AppImage'])

# Function for Settings action
def settings_pressed():
    global settings_json

    print("Settings activated!")
    settings.settings_menu()
    settings_json = load_json()

# Function for About action
def about_pressed():
    print("About activated!")
    about.about_screen()