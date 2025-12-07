import pygame
import json
import math
from ADCDACPi import ADCDACPi
import time
import RPi.GPIO as GPIO
from gpiozero import Button
import os
import serial
import threading

import serial

# Global variables
serial_brake = False
serial_clutch = False
serial_speed = 0.0
serial_rpm = 0

current_gear = -1
def read_serial():
    global serial_brake, serial_clutch, serial_speed, serial_rpm

    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)  # Update port if needed

    buffer = ""
    while True:
        if ser.in_waiting > 0:
            byte = ser.read().decode(errors="ignore")
            if byte == '\n':
                line = buffer.strip()
                buffer = ''
                if line:
                    try:
                        if len(line) >= 6:  # Minimum size check
                            brake_str  = line[-1]     # last char
                            clutch_str = line[-2]     # 2nd last char
                            rpm_str    = line[-6:-2]  # 4 chars before clutch/brake
                            speed_str  = line[:-6]    # everything else at the start

                            serial_speed  = float(speed_str)
                            serial_rpm    = int(rpm_str)
                            serial_clutch = (clutch_str == '1')
                            serial_brake  = (brake_str == '1')
                        else:
                            print(f"[Serial Parse Error] Incomplete line: {line}")
                    except Exception as e:
                        print(f"[Serial Parse Error] {line}: {e}")
            elif byte != '\r':
                buffer += byte

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

# GPIO pins
settings_json = load_json()
cruiseButtonLed_pin = settings_json["GPIO"]["cruiseButtonLed"]
cruiseButtonPressed_pin = settings_json["GPIO"]["cruiseButtonPressed"]
relay_pin = settings_json["GPIO"]["relays"]
max7219_din = settings_json["GPIO"]["max7219_din"]
max7219_cs = settings_json["GPIO"]["max7219_cs"]
max7219_clk = settings_json["GPIO"]["max7219_clk"]

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

last_throttle = 0

def GetThrottlePercentage() -> int:
    global last_throttle

    # Read raw throttle percentage from ADC
    raw_value = math.floor((adc.read_adc_voltage(1, 0) / 1.2 - 0.1) * 100)
    raw_value = max(0, min(100, raw_value))  # Clamp to 0–100%

    # Apply exponential moving average
    last_throttle = last_throttle + 0.2 * (raw_value - last_throttle)

    return int(last_throttle)

def GetClutch() -> bool:
    return not serial_clutch

def GetBrake() -> bool:
    return serial_brake
gears = [137,77,53,42,33,30]
def GetSpeed():
    gear = CalculateGear()
    if serial_speed < 30 or gear == -1:
        return serial_speed

    return GetRPM() / gears[gear-1]

def GetRPM():
    return serial_rpm

# speed multiplication to get RPM

def CalculateGear():
    global current_gear
    current_speed = serial_speed
    current_rpm = serial_rpm

    if current_rpm < 1000 or current_speed == 0 or GetClutch():
        current_gear = -1
        return -1

    # Calculate RPMs for each gear
    calculated_rpms = [current_speed * gear for gear in gears]

    # Find the index of the gear with the closest RPM
    best_gear_index = min(
        range(len(calculated_rpms)),
        key=lambda i: abs(calculated_rpms[i] - current_rpm)
    ) + 1

    if best_gear_index == 6:
        best_gear_index = -1

    current_gear = best_gear_index

    return best_gear_index

def GetGear():
    return current_gear

def SetRelays(value):
    # needs to be inverted
    GPIO.output(relay_pin, not value)

def GetButtonPressed():
    return not GPIO.input(cruiseButtonPressed_pin)

def SetButtonLed(value):
    GPIO.output(cruiseButtonLed_pin, value)
