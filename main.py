import pygame
import sys
import RPi.GPIO as GPIO
import subprocess

# Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dashboard")

# Fonts
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Gets called once
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.IN)

# Function to draw dashboard
def draw_dashboard(throttle, speed, clutch_pressed, brake_pressed):
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
    
    # Throttle
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (50, 150))
    pygame.draw.rect(screen, BUTTON_COLOR, (250, 150, throttle * 2, 30))
    
    # Speed
    speed_label = font_small.render("Speed", True, TEXT_COLOR)
    screen.blit(speed_label, (550, 150))
    if speed > 105:
        speed_text = font_small.render(f"{speed} km/h", True, (255, 0, 0))
    else:
        speed_text = font_small.render(f"{speed} km/h", True, TEXT_COLOR)
    screen.blit(speed_text, (800, 150))
    
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
    subprocess.run('./Carplay.AppImage', shell=True, executable="/bin/bash")

# Function for Settings action
def settings():
    print("Settings activated!")

# Function for About action
def about():
    print("About activated!")

# Main loop
def main():
    setup()

    throttle = 50  # Throttle percentage
    speed = 60     # Speed in km/h
    clutch_pressed = False
    brake_pressed = True
    
    clock = pygame.time.Clock()
    running = True
    
    # Set display mode to fullscreen
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
                    settings()
                # Check if the mouse click is within the About button area
                elif WIDTH - 150 <= event.pos[0] <= WIDTH - 50 and 50 <= event.pos[1] <= 50 + 30:
                    about()
        
        # Update dashboard
        draw_dashboard(throttle, speed, clutch_pressed, brake_pressed)
        
        # Adjust values for demonstration
        throttle += 1
        if throttle > 100:
            throttle = 0
        speed += 1
        if speed > 200:
            speed = 0
        clutch_pressed = GPIO.input(3)
        
        clock.tick(10)  # Limit frame rate
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
