import pygame
import sys
import time
import math
from Carviewer_global import *

# Variables
enabled = False

minSpeed = 30
maxSpeed = 150
desiredSpeed = minSpeed
voltageIntervene = 0.01
alpha = 0.0001

oldSpeed = [0] * 10
currentVoltage = 0.1
currentSpeed = 0

def cruise_control_screen():
    global enabled, oldSpeed, currentSpeed, desiredSpeed, currentVoltage

    running = True
    clock = pygame.time.Clock()

    while running:
        oldSpeed.append(currentSpeed)
        oldSpeed.pop(0)
        currentSpeed = GetSpeed()
        throttle = int((currentVoltage - 0.1) / 1.9 * 100)

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
                if 50 <= x <= 140:
                    if 400 <= y <= 450:
                        setDesiredSpeed(desiredSpeed - 1)
                    elif 460 <= y <= 510:
                        setDesiredSpeed(desiredSpeed - 5)

                if WIDTH - 140 <= x <= WIDTH - 50:
                    if 400 <= y <= 450:
                        setDesiredSpeed(desiredSpeed + 1)
                    elif 460 <= y <= 510:
                        setDesiredSpeed(desiredSpeed + 5)

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control", True, TEXT_COLOR)
        screen.blit(title_text, (50, 30))

        # Throttle Circle
        throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
        screen.blit(throttle_label, (50, 100))
        pygame.draw.circle(screen, TEXT_COLOR, (300, 200), 100, 3)
        pygame.draw.arc(screen, TEXT_COLOR, (200, 100, 200, 200),
                        3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)
        throttle_text = font_large.render(str(throttle), True, TEXT_COLOR)
        screen.blit(throttle_text, (300 - throttle_text.get_width() / 2, 200 - throttle_text.get_height() / 2))
        screen.blit(font_small.render("%", True, TEXT_COLOR), (325, 190))

        # Speed Circle
        speed_label = font_small.render("Speed", True, TEXT_COLOR)
        screen.blit(speed_label, (550, 100))
        pygame.draw.circle(screen, TEXT_COLOR, (800, 200), 100, 3)
        if currentSpeed > 105:
            speed_color = RED
        else:
            speed_color = TEXT_COLOR
        pygame.draw.arc(screen, speed_color, (700, 100, 200, 200),
                        3 * math.pi / 2 - (currentSpeed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
        speed_text = font_large.render(str(currentSpeed), True, speed_color)
        screen.blit(speed_text, (800 - speed_text.get_width() / 2, 200 - speed_text.get_height() / 2))
        screen.blit(font_small.render("km/h", True, TEXT_COLOR), (775, 225))

        # Desired Speed Text below throttle and speed
        desired_speed_text = font_large.render(f"Desired: {desiredSpeed} km/h", True, TEXT_COLOR)
        screen.blit(desired_speed_text, (WIDTH // 2 - desired_speed_text.get_width() // 2, 330))

        # Cruise Control toggle button
        cruise_control_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 220, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, cruise_control_rect)
        cruise_control_text = font_small.render("Disable Cruise" if enabled else "Enable Cruise", True, BUTTON_TEXT_COLOR)
        screen.blit(cruise_control_text, cruise_control_text.get_rect(center=cruise_control_rect.center))

        # Vertical Speed Adjustment Buttons
        button_size = (90, 50)

        # Left side (-5 and -1)
        left_buttons = [("-1", 400), ("-5", 460)]
        for label, y in left_buttons:
            rect = pygame.Rect(50, y, *button_size)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

        # Right side (+1 and +5)
        right_buttons = [("+1", 400), ("+5", 460)]
        for label, y in right_buttons:
            rect = pygame.Rect(WIDTH - 140, y, *button_size)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

        if enabled:
            cruise_control()
        else:
            reset()

        if not GetButtonPressed():
            reset()
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
        if deltaSpeed <= -desiredDifference * 0.2:
            currentVoltage += desiredDifference * voltageIntervene
        else:
            currentVoltage -= desiredDifference * voltageIntervene
    elif tooFast:
        if deltaSpeed >= -desiredDifference * 0.2:
            currentVoltage += desiredDifference * voltageIntervene
        else:
            currentVoltage -= desiredDifference * voltageIntervene
    else:
        if deltaSpeed < -0.05 or deltaSpeed > 0.05:
            currentVoltage += desiredDifference * voltageIntervene

    currentVoltage = max(min(currentVoltage, 2), minimalVoltage)

def setDesiredSpeed(value):
    global desiredSpeed
    desiredSpeed = max(min(value, maxSpeed), minSpeed)

def reset():
    global enabled
    SetRelays(False)
    SetThrottle(0)
    enabled = False

if __name__ == "__main__":
    cruise_control_screen()
