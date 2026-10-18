import pygame
import json
import math
import time
import sys
import random
from infobutton import InfoButton

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

# Colors
BACKGROUND_COLOR = (20, 20, 25)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
# The whole UI is authored in a DESIGN_WIDTH x DESIGN_HEIGHT design space and
# scaled to the real screen with S(), so it looks identical at any resolution.
DESIGN_WIDTH, DESIGN_HEIGHT = 1024, 576

# Fullscreen on the native resolution when started with the "fullscreen"
# argument (see start.sh), otherwise a design-sized window for desktop testing.
if "fullscreen" in sys.argv:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((DESIGN_WIDTH, DESIGN_HEIGHT))
pygame.display.set_caption("Carviewer 98-RS-RV")

WIDTH, HEIGHT = screen.get_size()
SCALE = min(WIDTH / DESIGN_WIDTH, HEIGHT / DESIGN_HEIGHT)

def S(value):
    # design-space pixels -> real screen pixels
    return round(value * SCALE)

# Fonts (sizes in design-space pixels)
font_super_large = pygame.font.Font(None, S(64))
font_large = pygame.font.Font(None, S(48))
font_small = pygame.font.Font(None, S(36))

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
    # hold the R key to simulate the engine being switched off
    if pygame.key.get_pressed()[pygame.K_r]:
        return 0
    old_rpm += 1
    return old_rpm

def GetGear():
    return 5

def SetRelays(value):
    pass
    # Dummy function: just print the relay state
    #print(f"SetRelays called with value: {value}")

info_button = InfoButton()

def _info_key_down():
    # hold the I key to simulate the info button
    return pygame.key.get_pressed()[pygame.K_i]

def GetInfoButtonOnPressed():
    # short press, fires on release
    return info_button.short_pressed(_info_key_down())

def GetInfoButtonCruiseShortPressed():
    # short press as seen by the cruise thread
    return info_button.cruise_short_pressed(_info_key_down())

def GetInfoButtonHeld():
    # True while the info button is down
    return info_button.held(_info_key_down())

def GetInfoButtonLongPressed():
    # number of long press ticks (one per second held, first at the long press threshold)
    return info_button.long_ticks(_info_key_down())

def GetButtonPressed():
    return False

def SetButtonLed(value):
    pass
    # Dummy function: print LED state
    #print(f"SetButtonLed called with value: {value}")
