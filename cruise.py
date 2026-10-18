import pygame
import sys
import time
import math
import subprocess
import threading
from Carviewer_Arduino import *

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

cruise_lock = threading.RLock()
idle = False

def cruise_control_screen(carplay):
    global enabled, oldSpeed, currentSpeed, desiredSpeed, currentVoltage, oldButtonState

    running = True
    clock = pygame.time.Clock()

    while running:
        throttle = int((currentVoltage - minimalVoltage) / 3.1 * 100)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Enable/Disable Cruise Control
                if (WIDTH // 2 - S(100)) <= x <= (WIDTH // 2 + S(100)) and (HEIGHT - S(180)) <= y <= (HEIGHT - S(130)):
                    set_cruise_control_enabled(not enabled)
                elif (WIDTH // 2 - S(100)) <= x <= (WIDTH // 2 + S(100)) and (HEIGHT - S(120)) <= y <= (HEIGHT - S(70)):
                    # Current speed button
                    setDesiredSpeed(currentSpeed)

                # Speed control buttons
                if S(50) <= x <= S(140):
                    if S(400) <= y <= S(450):
                        setDesiredSpeed(desiredSpeed - 1)
                    elif S(460) <= y <= S(510):
                        delta_5 = desiredSpeed % 5
                        setDesiredSpeed(desiredSpeed - 5 + (5-delta_5 if delta_5 > 2 else -delta_5))

                if WIDTH - S(140) <= x <= WIDTH - S(50):
                    if S(400) <= y <= S(450):
                        setDesiredSpeed(desiredSpeed + 1)
                    elif S(460) <= y <= S(510):
                        delta_5 = desiredSpeed % 5
                        setDesiredSpeed(desiredSpeed + 5 + (5-delta_5 if delta_5 > 2 else -delta_5))

        screen.fill(BACKGROUND_COLOR)

        # Title
        title_text = font_large.render("Cruise Control" if carplay == None else "CarPlay Mode", True, TEXT_COLOR)
        screen.blit(title_text, (S(50), S(50)))

        # Throttle Circle
        throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
        screen.blit(throttle_label, (S(50), S(150)))
        pygame.draw.circle(screen, TEXT_COLOR, (S(300), S(200)), S(100), S(3))
        pygame.draw.arc(screen, TEXT_COLOR, (S(200), S(100), S(200), S(200)),
                        3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, S(10))
        throttle_text = font_large.render(str(throttle), True, TEXT_COLOR)
        screen.blit(throttle_text, (S(300) - throttle_text.get_width() / 2, S(200) - throttle_text.get_height() / 2))
        screen.blit(font_small.render("%", True, TEXT_COLOR), (S(325), S(190)))

        # Speed Circle
        speed_label = font_small.render("Speed", True, TEXT_COLOR)
        screen.blit(speed_label, (S(550), S(150)))
        pygame.draw.circle(screen, TEXT_COLOR, (S(800), S(200)), S(100), S(3))
        if currentSpeed > 105:
            speed_color = RED
        else:
            speed_color = TEXT_COLOR
        pygame.draw.arc(screen, speed_color, (S(700), S(100), S(200), S(200)),
                        3 * math.pi / 2 - (currentSpeed / 200) * 2 * math.pi, 3 * math.pi / 2, S(10))
        speed_text = font_large.render(str(int(currentSpeed)), True, speed_color)
        screen.blit(speed_text, (S(800) - speed_text.get_width() / 2, S(200) - speed_text.get_height() / 2))
        screen.blit(font_small.render("km/h", True, TEXT_COLOR), (S(775), S(225)))

        # Desired Speed Text below throttle and speed
        desired_speed_text = font_large.render(f"Desired: {int(desiredSpeed)} km/h", True, TEXT_COLOR)
        screen.blit(desired_speed_text, (WIDTH // 2 - desired_speed_text.get_width() // 2, S(330)))

        # Cruise Control toggle button
        cruise_control_rect = pygame.Rect(WIDTH // 2 - S(100), HEIGHT - S(180), S(200), S(50))
        pygame.draw.rect(screen, BUTTON_COLOR, cruise_control_rect)
        cruise_control_text = font_small.render("Disable Cruise" if enabled else "Enable Cruise", True, BUTTON_TEXT_COLOR)
        screen.blit(cruise_control_text, cruise_control_text.get_rect(center=cruise_control_rect.center))

        # Current speed button
        current_speed_rect = pygame.Rect(WIDTH // 2 - S(100), HEIGHT - S(120), S(200), S(50))
        pygame.draw.rect(screen, BUTTON_COLOR, current_speed_rect)
        current_speed_text = font_small.render("Current Speed", True, BUTTON_TEXT_COLOR)
        screen.blit(current_speed_text, current_speed_text.get_rect(center=current_speed_rect.center))

        # Vertical Speed Adjustment Buttons
        button_size = (S(90), S(50))

        # Left side (-5 and -1)
        left_buttons = [("-1", S(400)), ("-5", S(460))]
        for label, y in left_buttons:
            rect = pygame.Rect(S(50), y, *button_size)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))

        # Right side (+1 and +5)
        right_buttons = [("+1", S(400)), ("+5", S(460))]
        for label, y in right_buttons:
            rect = pygame.Rect(WIDTH - S(140), y, *button_size)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text = font_small.render(label, True, BUTTON_TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))


        if carplay == None:
            if not GetButtonPressed():
                reset()
                return # back to read.py

        else:
            # Carplay-cruise control mode
            #carviewer = find_window_by_title(i3, "Carviewer 98-RS-RV")
            if carplay.poll() == None:
                # Carplay still running

                # Only update on Press/Unpress
                currentButtonState = GetButtonPressed()
                if oldButtonState != currentButtonState:
                    #electron = find_window_by_title(i3, "Electron")

                    if currentButtonState:
                       pass
                        #carviewer.command("fullscreen enable")
                        #electron.command('move to scratchpad')
                    else:
                       pass
                        #electron.command('scratchpad show')
                        #electron.command("fullscreen enable")

                    oldButtonState = currentButtonState
            else:
                # Carplay terminated, exit Carplay-cruise control mode
                #carviewer.command("fullscreen enable")
                reset()
                return

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def cruise_tick():
    # Runs on every frame in the background, whatever screen is shown
    global currentSpeed

    with cruise_lock:
        oldSpeed.append(currentSpeed)
        oldSpeed.pop(0)
        currentSpeed = GetSpeed()

        shortPress = GetInfoButtonCruiseShortPressed()
        longTicks = GetInfoButtonLongPressed()

        # short press disables
        if shortPress and enabled:
            set_cruise_control_enabled(False)

        # holding: first tick enables, every tick after that (or every tick while already enabled) adds 1 km/h
        for _ in range(longTicks):
            if not enabled:
                set_cruise_control_enabled(True)
                setDesiredSpeed(currentSpeed)
            else:
                setDesiredSpeed(desiredSpeed + 1)

        if enabled:
            cruise_control()
        elif not idle:
            reset()

def cruise_loop():
    clock = pygame.time.Clock()
    while True:
        cruise_tick()
        clock.tick(30)

def start_cruise_thread():
    threading.Thread(target=cruise_loop, daemon=True).start()

def set_cruise_control_enabled(enable):
    global enabled, currentVoltage, idle
    with cruise_lock:
        if enable:
            if GetSpeed() < 30:
                return

            enabled = True
            idle = False
            currentVoltage = GetThrottle() * 2  # DAC output needs twice the pedal ADC voltage

        else:
            reset()

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

    currentVoltage = max(min(3.29, currentVoltage), minimalVoltage)

def setDesiredSpeed(value):
    global desiredSpeed
    desiredSpeed = max(min(value, maxSpeed), minSpeed)
    desiredSpeed = int(desiredSpeed) + 0.5

def reset():
    global enabled, currentVoltage, ledInterval, buttonLed, idle
    with cruise_lock:
        SetRelays(False)
        SetThrottle(minimalVoltage)
        currentVoltage = minimalVoltage
        enabled = False
        idle = True
        ledInterval = 0
        buttonLed = True
        SetButtonLed(buttonLed)

if __name__ == "__main__":
    cruise_control_screen()
