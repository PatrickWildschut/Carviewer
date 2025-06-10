import pygame
import sys
import time
import math
import subprocess
import i3ipc
from Carviewer_global import *

# Variables
enabled = False

minSpeed = 30
maxSpeed = 150
desiredSpeed = minSpeed
voltageIntervene = 0.008
alpha = 0.0001

oldSpeed = [0] * 10
currentVoltage = minimalVoltage
currentSpeed = 0

ledInterval = 0
buttonLed = True
oldButtonState = False

i3 = i3ipc.Connection()

def find_window_by_class(i3, class_name):
    return next(
        (w for w in i3.get_tree().leaves() if w.window_class == class_name),
        None
    )

def cruise_control_screen(carplay):
    global enabled, oldSpeed, currentSpeed, desiredSpeed, currentVoltage, oldButtonState

    running = True
    clock = pygame.time.Clock()

    while running:
        oldSpeed.append(currentSpeed)
        oldSpeed.pop(0)
        currentSpeed = GetSpeed()
        throttle = int((currentVoltage - minimalVoltage) / 3.1 * 100)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Enable/Disable Cruise Control
                if (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 180) <= y <= (HEIGHT - 130):
                    enabled = not enabled
                    currentVoltage = GetThrottle() * 2
                elif (WIDTH // 2 - 100) <= x <= (WIDTH // 2 + 100) and (HEIGHT - 120) <= y <= (HEIGHT - 70):
                    # Current speed button
                    setDesiredSpeed(currentSpeed)

                # Speed control buttons
                if 50 <= x <= 140:
                    if 400 <= y <= 450:
                        setDesiredSpeed(desiredSpeed - 1)
                    elif 460 <= y <= 510:
                        delta_5 = desiredSpeed % 5
                        setDesiredSpeed(desiredSpeed - 5 + (5-delta_5 if delta_5 > 2 else -delta_5))

                if WIDTH - 140 <= x <= WIDTH - 50:
                    if 400 <= y <= 450:
                        setDesiredSpeed(desiredSpeed + 1)
                    elif 460 <= y <= 510:
                        delta_5 = desiredSpeed % 5
                        setDesiredSpeed(desiredSpeed + 5 + (5-delta_5 if delta_5 > 2 else -delta_5))

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # Throttle Circle
        throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
        screen.blit(throttle_label, (50, 150))
        pygame.draw.circle(screen, TEXT_COLOR, (300, 200), 100, 3)
        pygame.draw.arc(screen, TEXT_COLOR, (200, 100, 200, 200),
                        3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)
        throttle_text = font_large.render(str(throttle), True, TEXT_COLOR)
        screen.blit(throttle_text, (300 - throttle_text.get_width() / 2, 200 - throttle_text.get_height() / 2))
        screen.blit(font_small.render("%", True, TEXT_COLOR), (325, 190))

        # Speed Circle
        speed_label = font_small.render("Speed", True, TEXT_COLOR)
        screen.blit(speed_label, (550, 150))
        pygame.draw.circle(screen, TEXT_COLOR, (800, 200), 100, 3)
        if currentSpeed > 105:
            speed_color = RED
        else:
            speed_color = TEXT_COLOR
        pygame.draw.arc(screen, speed_color, (700, 100, 200, 200),
                        3 * math.pi / 2 - (currentSpeed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
        speed_text = font_large.render(str(int(currentSpeed)), True, speed_color)
        screen.blit(speed_text, (800 - speed_text.get_width() / 2, 200 - speed_text.get_height() / 2))
        screen.blit(font_small.render("km/h", True, TEXT_COLOR), (775, 225))

        # Desired Speed Text below throttle and speed
        desired_speed_text = font_large.render(f"Desired: {int(desiredSpeed)} km/h", True, TEXT_COLOR)
        screen.blit(desired_speed_text, (WIDTH // 2 - desired_speed_text.get_width() // 2, 330))

        # Cruise Control toggle button
        cruise_control_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 180, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, cruise_control_rect)
        cruise_control_text = font_small.render("Disable Cruise" if enabled else "Enable Cruise", True, BUTTON_TEXT_COLOR)
        screen.blit(cruise_control_text, cruise_control_text.get_rect(center=cruise_control_rect.center))

        # Current speed button
        current_speed_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, current_speed_rect)
        current_speed_text = font_small.render("Current Speed", True, BUTTON_TEXT_COLOR)
        screen.blit(current_speed_text, current_speed_text.get_rect(center=current_speed_rect.center))

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

        if carplay == None:
            if not GetButtonPressed():
                reset()
                return # back to read.py

        else:
            # Carplay-cruise control mode
            if carplay.poll() == None:
                # Carplay still running

                # Only update on Press/Unpress
                currentButtonState = GetButtonPressed()
                if oldButtonState != currentButtonState:
                    electron = find_window_by_class(i3, "Electron")
                    #carviewer = find_window_by_class(i3, "Carviewer 98-RS-RV")

                    if currentButtonState:
                        electron.command('move to scratchpad')
                    else:
                        # carplay window
                        electron.command('scratchpad show')
                        electron.command("fullscreen enable")

                    oldButtonState = currentButtonState
            else:
                # Carplay terminated, exit Carplay-cruise control mode
                reset()
                return

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def cruise_control():
    global enabled, ledInterval, buttonLed

    if checkPedalsPressed():
        enabled = False
        return

    calculateNewVoltage()
    SetThrottle(currentVoltage)
    SetRelays(True)

    ledInterval += 1

    if ledInterval == 30:
        buttonLed = not buttonLed
        SetButtonLed(buttonLed)
        ledInterval = 0

def checkPedalsPressed() -> bool:
    return GetClutch() or GetBrake()

def map_value(x, in_min, in_max, out_min, out_max):
    if x < in_min:
        return out_min
    elif x > in_max:
        return out_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

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

    currentVoltage = max(min(currentVoltage, map_value(abs(desiredDifference), 2, 10, 2, 3.3)), minimalVoltage)

def setDesiredSpeed(value):
    global desiredSpeed
    desiredSpeed = max(min(value, maxSpeed), minSpeed)
    desiredSpeed = int(desiredSpeed) + 0.5

def reset():
    global enabled, currentVoltage, ledInterval, buttonLed
    SetRelays(False)
    SetThrottle(minimalVoltage)
    currentVoltage = minimalVoltage
    enabled = False
    ledInterval = 0
    buttonLed = True
    SetButtonLed(buttonLed)

if __name__ == "__main__":
    cruise_control_screen()
