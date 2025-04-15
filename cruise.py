import pygame
import sys
import time
from Carviewer_global import *

# Variables
enabled = False

minSpeed = 30
desiredSpeed = minSpeed
voltageIntervene = 0.01
alpha = 0.0001

oldSpeed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
currentVoltage = 0.5

# Will be updated in cruise_control_screen
currentSpeed = 0

def cruise_control_screen():
    global enabled, oldSpeed, currentSpeed, desiredSpeed, currentVoltage

    running = True
    clock = pygame.time.Clock()

    while running:
        oldSpeed.append(currentSpeed)
        oldSpeed.pop(0)
        currentSpeed = GetSpeed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Enable/Disable Cruise Control
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 220) <= y <= (HEIGHT - 170):
                    enabled = not enabled
                    currentVoltage = GetThrottle() * 2

                # Speed control buttons
                if (WIDTH // 2 - 225) <= x <= (WIDTH // 2 - 135) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    setDesiredSpeed(desiredSpeed - 5)

                if (WIDTH // 2 - 115) <= x <= (WIDTH // 2 - 25) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    setDesiredSpeed(desiredSpeed - 1)

                if (WIDTH // 2 + 25) <= x <= (WIDTH // 2 + 115) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    setDesiredSpeed(desiredSpeed + 1)

                if (WIDTH // 2 + 135) <= x <= (WIDTH // 2 + 225) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    setDesiredSpeed(desiredSpeed + 5)

                # Current Speed Button
                if (WIDTH // 2 + 245) <= x <= (WIDTH // 2 + 435) and (HEIGHT - 100) <= y <= (HEIGHT - 50):
                    setDesiredSpeed(currentSpeed)

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))
        
        # Current and Desired Speeds
        current_speed_text = font_large.render(f"Current: {currentSpeed} km/h", True, TEXT_COLOR)
        desired_speed_text = font_large.render(f"Desired: {desiredSpeed} km/h", True, TEXT_COLOR)
        screen.blit(current_speed_text, (WIDTH // 2 - 300, 150))
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
            ("-5", WIDTH // 2 - 225),
            ("-1", WIDTH // 2 - 115),
            ("+1", WIDTH // 2 + 25),
            ("+5", WIDTH // 2 + 135)
        ]

        for label, x_pos in speed_buttons:
            rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

        # Current Speed Set button
        rect = pygame.Rect(WIDTH // 2 + 245, y_pos, button_width * 2, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        text = font_small.render("Current Speed", True, BUTTON_TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))

        if enabled:
            cruise_control()
        else:
            reset()

        if not GetButtonPressed():
            return # back to read.py

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def cruise_control():
    global enabled

    if checkPedalsPressed():
        enabled = False
        return

    calculateNewVoltage()
    SetThrottle(currentVoltage)
    SetRelays(True)

def checkPedalsPressed() -> bool:
    return GetClutch() or GetBrake()

def calculateNewVoltage():
    global currentVoltage, desiredSpeed, voltageIntervene
    desiredDifference = desiredSpeed - currentSpeed
    deltaSpeed = oldSpeed[0] - currentSpeed

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

    #gradient = -1 * desiredDifference * deltaSpeed
    #voltageIntervene -= alpha * gradient

    voltageIntervene = max(min(voltageIntervene, 0.1), 0.0001)
    currentVoltage = max(min(currentVoltage, 2), 0.1)

def setDesiredSpeed(value):
    global desiredSpeed

    if value < minSpeed:
        desiredSpeed = minSpeed
    else:
        desiredSpeed = value

def reset():
    SetRelays(False)
    SetThrottle(0)

if __name__ == "__main__":
    cruise_control_screen()
