import pygame
import json
import math
from ADCDACPi import ADCDACPi
import time
import pigpio
import RPi.GPIO as GPIO
from gpiozero import Button
import os
import serial
import threading

# Shared variables for serial input
serial_brake = False
serial_clutch = False
serial_speed = 0.0
serial_rpm = 0

def read_serial():
    global serial_brake, serial_clutch, serial_speed, serial_rpm

    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)  # Update to your port

    buffer = ""
    while True:
        if ser.in_waiting > 0:
            byte = ser.read().decode(errors='ignore')
            if byte == '\n':
                line = buffer.strip()
                buffer = ''
                if line:
                    try:
                        prefix = line[0]
                        value = line[1:]
                        if prefix == 'b':
                            serial_brake = value == '1'
                        elif prefix == 'c':
                            serial_clutch = value == '1'
                        elif prefix == 's':
                            serial_speed = float(value)
                        elif prefix == 'r':
                            serial_rpm = int(float(value))
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

def GetThrottlePercentage() -> int:
    value = math.floor((adc.read_adc_voltage(1, 0) / 1.4 - 0.1) * 100)

    if value > 100:
        return 100
    elif value < 0:
        return 0

    return value

def GetClutch() -> bool:
    return serial_clutch

def GetBrake() -> bool:
    return serial_brake

def GetSpeed():
    return serial_speed

def GetRPM():
    return serial_rpm

# speed multiplication to get RPM
gears = [137, 77, 53, 42, 33, 30]

def GetGear():
    current_speed = GetSpeed()
    current_rpm = GetRPM()

    if current_rpm < 1000 or current_speed == 0 or GetClutch():
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
    
    return best_gear_index

def SetRelays(value):
    # needs to be inverted
    GPIO.output(relay_pin, not value)

def GetButtonPressed():
    return not GPIO.input(cruiseButtonPressed_pin)

def SetButtonLed(value):
    GPIO.output(cruiseButtonLed_pin, value)