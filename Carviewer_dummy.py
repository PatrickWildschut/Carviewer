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

def GetThrottlePercentage() -> int:
    # Simulate a percentage from 0 to 100
    return random.randint(0, 100)

def GetClutch() -> bool:
    # Randomly simulate clutch being pressed or not
    return False

def GetBrake() -> bool:
    # Randomly simulate brake being pressed or not
    return False

def GetSpeed():
    # Simulate a speed between 0 and 120 km/h
    return 113

old_rpm = 1000
def GetRPM():
    global old_rpm
    old_rpm += 1
    return old_rpm

def GetGear():
    return 3

def SetRelays(value):
    pass
    # Dummy function: just print the relay state
    #print(f"SetRelays called with value: {value}")

def GetButtonPressed():
    # Randomly simulate button pressed
    return False

def SetButtonLed(value):
    pass
    # Dummy function: print LED state
    #print(f"SetButtonLed called with value: {value}")
