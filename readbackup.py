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
    
    # NOTE: fullscreen is set up at startup by Carviewer_global (based on the
    # "fullscreen" command line argument), so the screen surface stays valid.

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the Apple Carplay button area
                if S(50) <= event.pos[0] <= S(50) + S(200) and S(500) <= event.pos[1] <= S(500) + S(50):
                    apple_carplay()
                # Check if the mouse click is within the Settings button area
                elif WIDTH - S(50) - S(200) <= event.pos[0] <= WIDTH - S(50) and S(500) <= event.pos[1] <= S(500) + S(50):
                    settings_pressed()
                # Check if the mouse click is within the About button area
                elif WIDTH - S(150) <= event.pos[0] <= WIDTH - S(50) and S(50) <= event.pos[1] <= S(50) + S(30):
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
    screen.blit(title_text, (S(50), S(50)))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - S(150), S(50), S(100), S(30))
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
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, S(550)))
    
    # Throttle
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (S(50), S(150)))
    pygame.draw.rect(screen, BUTTON_COLOR, (S(250), S(150), throttle * 2 * SCALE, S(30)))
    
    # Speed
    # speed_label = font_small.render("Speed", True, TEXT_COLOR)
    # screen.blit(speed_label, (S(550), S(150)))
    # if speed > 105:
    #     speed_text = font_small.render(f"{speed} km/h", True, (255, 0, 0))
    # else:
    #     speed_text = font_small.render(f"{speed} km/h", True, TEXT_COLOR)
    # screen.blit(speed_text, (S(800), S(150)))
    
    pygame.draw.circle(screen, TEXT_COLOR, (S(150), S(150)), S(100), S(3))
    pygame.draw.arc(screen, TEXT_COLOR, (S(75), S(75), S(150), S(150)), 3 * 3.14 / 4, 3 * 3.14 / 4 + speed * 3.14 / 200, S(10))
    speed_text = font_large.render(str(speed), True, TEXT_COLOR)
    screen.blit(speed_text, (S(135) - speed_text.get_width() / 2, S(140) - speed_text.get_height() / 2))
    pygame.draw.rect(screen, TEXT_COLOR, (S(130), S(200), S(40), S(3)))
    
    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (S(50), S(300)))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, (255, 0, 0) if clutch_pressed else (0, 255, 0))
    screen.blit(clutch_text, (S(300), S(300)))
    
    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (S(550), S(300)))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, (255, 0, 0) if brake_pressed else (0, 255, 0))
    screen.blit(brake_text, (S(800), S(300)))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (S(50), S(200)), (S(950), S(200)), S(2))
    pygame.draw.line(screen, TEXT_COLOR, (S(50), S(350)), (S(950), S(350)), S(2))
    
    # Draw buttons
    button_width = S(200)
    button_height = S(50)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (S(50), S(500), button_width, button_height))
    apple_carplay_text = font_small.render("Apple Carplay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(S(50) + button_width // 2, S(500) + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - S(50) - button_width, S(500), button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - S(50) - button_width // 2, S(500) + button_height // 2))
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