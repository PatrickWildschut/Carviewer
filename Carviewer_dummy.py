import pygame
import json
import math
import time
import random

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

# Load settings
settings_json = load_json()
fps = settings_json["Program"]["fps"]
minimalVoltage = 0.2

# Initialize Pygame
pygame.display.init()
pygame.font.init()

# Fonts
font_super_large = pygame.font.Font(None, 64)
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Colors
BACKGROUND_COLOR = (20, 20, 25)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carviewer 98-RS-RV")

# --- Dummy implementations below ---

def GetThrottle() -> float:
    # Return a random voltage between 0 and 3.3V
    return 1.2

def SetThrottle(value):
    pass
    # Dummy function: just print the value
    #print(f"SetThrottle called with value: {value}")

last_throttle = 0
def GetThrottlePercentage() -> int:
    global last_throttle

    # Read raw throttle percentage from ADC
    raw_value = math.floor(random.randint(0,100))
    raw_value = max(0, min(100, raw_value))  # Clamp to 0–100%

    # Apply exponential moving average
    last_throttle = last_throttle + 0.2 * (raw_value - last_throttle)

    return int(last_throttle)

def GetClutch() -> bool:
    # Randomly simulate clutch being pressed or not
    return False

def GetBrake() -> bool:
    # Randomly simulate brake being pressed or not
    return False

gears = [137,77,53,42,33,30]

old_rpm = 5000

def GetSpeed():
    global old_rpm
    return old_rpm / 53

def GetRPM():
    global old_rpm
    old_rpm += 1
    return old_rpm

def GetGear():
    return 5

def SetRelays(value):
    pass
    # Dummy function: just print the relay state
    #print(f"SetRelays called with value: {value}")

infowait = 0
def GetInfoButtonOnPressed():
    global infowait
    infowait += 1

    if infowait > 50:
        infowait = 0
        return True
    
    return False

def GetButtonPressed():
    return False

def SetButtonLed(value):
    pass
    # Dummy function: print LED state
    #print(f"SetButtonLed called with value: {value}")
