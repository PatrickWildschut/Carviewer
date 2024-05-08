import pygame
import subprocess
import json
import math
from ADCDACPi import ADCDACPi
import RPi.GPIO as GPIO

# Initialize Pygame
pygame.init()

# Fonts
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carviewer 98-RS-RV")

# ADC DAC
adc = ADCDACPi(1)
adc.set_adc_refvoltage(3.3)

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

# Save GPIO pins
settings_json = load_json()
clutch_pin = settings_json["GPIO"]["clutch"]
brake_pin = settings_json["GPIO"]["brake"]
speed_pin = settings_json["GPIO"]["speed"]

# GPIO

def GetThrottle() -> float:
    return adc.read_adc_voltage(1, 0)

def GetThrottlePercentage() -> int:
    value = math.floor(adc.read_adc_voltage(1, 0) / 1.6 * 100)

    if value > 100:
        return 100
    elif value < 0:
        return 0

    return value

def GetClutch() -> bool:
    return not GPIO.input(clutch_pin)

def GetBrake() -> bool:
    return GPIO.input(brake_pin)

def GetSpeed() -> float:
    return 10#GPIO.wait_for_edge(speed_pin, GPIO.RISING, timeout=500)
