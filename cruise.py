import pygame
import sys
import time
from Carviewer_global import *

# Variables
enabled = False

desiredSpeed = 0
minSpeed = 30
voltageIntervene = 0.1


oldSpeed = 0
currentVoltage = 0.5

# Will be updated in cruise_control_screen
currentSpeed = 0

def cruise_control_screen():
    global enabled, oldSpeed, currentSpeed, desiredSpeed

    running = True
    clock = pygame.time.Clock()

    while running:

        oldSpeed = currentSpeed
        currentSpeed = GetSpeed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Enable/Disable Cruise Control
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 220) <= y <= (HEIGHT - 170):
                    enabled = not enabled

                # Increase desired speed by 5
                if (WIDTH // 2 - 210) <= x <= (WIDTH // 2 - 120) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    desiredSpeed += 5

                # Increase desired speed by 1
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 - 10) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    desiredSpeed += 1

                # Decrease desired speed by 1
                if (WIDTH // 2 + 10) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    desiredSpeed -= 1

                # Decrease desired speed by 5
                if (WIDTH // 2 + 120) <= x <= (WIDTH // 2 + 210) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    desiredSpeed -= 5

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control", True, TEXT_COLOR)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 50)))

        # Current and Desired Speeds
        current_speed_text = font_large.render(f"{currentSpeed} km/h", True, TEXT_COLOR)
        desired_speed_text = font_large.render(f"Desired: {desiredSpeed} km/h", True, TEXT_COLOR)
        screen.blit(current_speed_text, (WIDTH // 2 - 200, 150))
        screen.blit(desired_speed_text, (WIDTH // 2 + 50, 150))

        # Cruise Control toggle button
        cruise_control_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 220, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, cruise_control_rect)
        cruise_control_text = font_small.render(
            "Disable Cruise" if enabled else "Enable Cruise", True, BUTTON_TEXT_COLOR
        )
        screen.blit(cruise_control_text, cruise_control_text.get_rect(center=cruise_control_rect.center))

        # Desired speed adjustment buttons
        button_width = 90
        button_height = 50
        y_pos = HEIGHT - 100
        speed_buttons = [
            ("+5", WIDTH // 2 - 210),
            ("+1", WIDTH // 2 - 100),
            ("-1", WIDTH // 2 + 10),
            ("-5", WIDTH // 2 + 120)
        ]

        for label, x_pos in speed_buttons:
            rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

        if enabled:
            cruise_control()

        if not GetButtonPressed():
            return # return to main.py

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def cruise_control():
    global enabled

    # Pedals check
    if checkPedalsPressed():
        enabled = False
        reset()
        return

    # Add throttle take over TODO

    calculateNewVoltage()
    SetThrottle(currentVoltage)
    SetRelays(True)

def checkPedalsPressed() -> bool:
    return GetClutch() or GetBrake()

def calculateNewVoltage():
    global currentVoltage
    desiredDifference = desiredSpeed - currentSpeed
    deltaSpeed = oldSpeed - currentSpeed

    tooSlow = desiredDifference < 0
    tooFast = desiredDifference > 0

    if tooSlow:
        if deltaSpeed <= -desiredDifference * 0.1:
            currentVoltage += desiredDifference * voltageIntervene
        else:
            currentVoltage -= desiredDifference * voltageIntervene
    elif tooFast:
        if deltaSpeed >= -desiredDifference * 0.1:
            currentVoltage += desiredDifference * voltageIntervene
        else:
            currentVoltage -= desiredDifference * voltageIntervene
        
    else:
        if deltaSpeed < -0.05 or deltaSpeed > 0.05:
            currentVoltage += desiredDifference * voltageIntervene

    if currentVoltage > 2:
        currentVoltage = 2;
    elif currentVoltage < 0:
        currentVoltage = 0

def reset():
    SetRelays(False)
    SetThrottle(0)
    
if __name__ == "__main__":
    cruise_control_screen()
