import pygame
import json
import math
from ADCDACPi import ADCDACPi
import time
import pigpio
import RPi.GPIO as GPIO

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

# GPIO pins
settings_json = load_json()
clutch_pin = settings_json["GPIO"]["clutch"]
brake_pin = settings_json["GPIO"]["brake"]
speed_pin = settings_json["GPIO"]["speedPWM"]
cruiseButtonLed_pin = settings_json["GPIO"]["cruiseButtonLed"]
cruiseButtonPressed_pin = settings_json["GPIO"]["cruiseButtonPressed"]
relay1_pin = settings_json["GPIO"]["relay1"]
relay2_pin = settings_json["GPIO"]["relay2"]
fps = settings_json["Program"]["fps"]


# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon")
    time.sleep(1)
    exit()

# Set the pin to input mode
pi.set_mode(speed_pin, pigpio.INPUT)
pi.set_glitch_filter(speed_pin, 1000)
last_tick = None
period = None

def pwm_callback(gpio, level, tick):
    global last_tick, period
    if last_tick is not None:
        period = pigpio.tickDiff(last_tick, tick)
    last_tick = tick

speed_from_gpio = pi.callback(speed_pin, pigpio.RISING_EDGE, pwm_callback)
#cb = pi.callback(rpm_pin, pigpio.RISING_EDGE, pwm_callback)

# Initialize Pygame
pygame.display.init()
pygame.font.init()
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

# GPIO

def GetThrottle() -> float:
    return adc.read_adc_voltage(1, 0)

def SetThrottle(value):
    if value < 0:
        value = 0
    elif value > 2:
        value = 2

    adc.set_dac_voltage(1, value)

def GetThrottlePercentage() -> int:
    value = math.floor((adc.read_adc_voltage(1, 0) / 1.4 - 0.1) * 100)

    if value > 100:
        return 100
    elif value < 0:
        return 0

    return value

def GetClutch() -> bool:
    return not GPIO.input(clutch_pin)

def GetBrake() -> bool:
    return GPIO.input(brake_pin)

def GetSpeed():
    if period is not None:
        frequency = 1000000 / period
        speed = frequency * 0.73

        if speed < 5:
            return 0

        return round(speed, 2)
    
    return 0

def SetRelays(value):
    # needs to be inverted
    GPIO.output(relay1_pin, not value)
    GPIO.output(relay2_pin, not value)

def GetButtonPressed():
    return not GPIO.input(cruiseButtonPressed_pin)

def SetButtonLed(value):
    GPIO.output(cruiseButtonLed_pin, value)