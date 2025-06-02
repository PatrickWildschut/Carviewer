import pygame
import json
import math
from ADCDACPi import ADCDACPi
import time
import pigpio
import RPi.GPIO as GPIO
from gpiozero import Button
import os

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

# GPIO pins
settings_json = load_json()
clutch_pin = settings_json["GPIO"]["clutch"]
brake_pin = settings_json["GPIO"]["brake"]
speed_pin = settings_json["GPIO"]["speedPWM"]
rpm_pin = settings_json["GPIO"]["rpmPWM"]
cruiseButtonLed_pin = settings_json["GPIO"]["cruiseButtonLed"]
cruiseButtonPressed_pin = settings_json["GPIO"]["cruiseButtonPressed"]
relay1_pin = settings_json["GPIO"]["relay1"]
relay2_pin = settings_json["GPIO"]["relay2"]
fps = settings_json["Program"]["fps"]

minimalVoltage = 0.2

# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon")
    time.sleep(1)
    exit()

# Set the pin to input mode
pi.set_mode(speed_pin, pigpio.INPUT)
pi.set_mode(rpm_pin, pigpio.INPUT)
pi.set_glitch_filter(speed_pin, 1000)
pi.set_glitch_filter(rpm_pin, 1000)
last_tick_speed = None
last_tick_rpm = None
period_speed = None
period_rpm = None

def pwm_callback_speed(gpio, level, tick):
    global last_tick_speed, period_speed
    if last_tick_speed is not None:
        period_speed = pigpio.tickDiff(last_tick_speed, tick)
    last_tick_speed = tick

def pwm_callback_rpm(gpio, level, tick):
    global last_tick_rpm, period_rpm
    if last_tick_rpm is not None:
        period_rpm = pigpio.tickDiff(last_tick_rpm, tick)
    last_tick_rpm = tick

speed_from_gpio = pi.callback(speed_pin, pigpio.RISING_EDGE, pwm_callback_speed)
rpm_from_gpio = pi.callback(rpm_pin, pigpio.RISING_EDGE, pwm_callback_rpm)

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

# ADC DAC
adc = ADCDACPi(2)
adc.set_adc_refvoltage(3.3)

# GPIO

def GetThrottle() -> float:
    return adc.read_adc_voltage(1, 0)

def SetThrottle(value):
    if value < 0:
        value = 0
    elif value > 3.29:
        value = 3.29

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
    if period_speed is not None:
        frequency = 1000000 / period_speed
        speed = frequency * 0.73

        if speed < 5:
            return 0

        return round(speed, 2)
    
    return 0


old_rpm = [0] * 30
def GetRPM():
    global old_rpm

    if period_rpm is not None:
        frequency = 1000000 / period_rpm

        rpm = frequency * 60
        old_rpm.append(rpm)
        old_rpm.pop(0)

        if old_rpm[0] != rpm or GetSpeed() > 0:
            return int(rpm)

    return 0

# speed multiplication to get RPM
gears = [150, 75, 52, 43, 34, 25]

def GetGear():
    current_speed = GetSpeed()
    current_rpm = GetRPM()

    if current_rpm < 1000 or current_speed == 0:
        return -1

    # Calculate RPMs for each gear
    calculated_rpms = [current_speed * gear for gear in gears]

    # Find the index of the gear with the closest RPM
    best_gear_index = min(
        range(len(calculated_rpms)),
        key=lambda i: abs(calculated_rpms[i] - current_rpm)
    ) + 1

    if best_gear_index == 6 or GetClutch():
        best_gear_index = -1
    
    return best_gear_index

def SetRelays(value):
    # needs to be inverted
    GPIO.output(relay1_pin, not value)
    GPIO.output(relay2_pin, not value)

def GetButtonPressed():
    return not GPIO.input(cruiseButtonPressed_pin)

def SetButtonLed(value):
    GPIO.output(cruiseButtonLed_pin, value)