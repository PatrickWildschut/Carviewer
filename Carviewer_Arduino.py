import pygame
import json
import math
from ADCDACPi import ADCDACPi
import time
import sys
import RPi.GPIO as GPIO
from gpiozero import Button
import os
import serial
import threading
from infobutton import InfoButton

# SDL defaults to the x11 driver when both DISPLAY and WAYLAND_DISPLAY are set,
# and through XWayland its fullscreen surface ends up in a format that
# SDL_FillRects() rejects ("Unsupported surface format" crashes). Use the
# native Wayland driver instead, unless it is explicitly overridden.
os.environ.setdefault("SDL_VIDEODRIVER", "wayland")

# ADC/DAC share one SPI bus and are used from multiple threads
adc_lock = threading.Lock()

# Global variables
serial_info_button = False
serial_brake = False
serial_clutch = False
serial_speed = 0.0
serial_rpm = 0

current_gear = -1

# The Arduino can re-enumerate on another port after a USB reset/power dip
SERIAL_PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
SERIAL_RETRY_DELAY = 1  # seconds between reconnect attempts
SERIAL_STALL_TIMEOUT = 3  # seconds without a full line before reconnecting

def open_serial():
    # Keep trying until one of the ports opens
    while True:
        for port in SERIAL_PORTS:
            try:
                ser = serial.Serial(port, 115200, timeout=0.1)
                print(f"[Serial] Connected to {port}")
                return ser
            except (serial.SerialException, OSError):
                pass
        time.sleep(SERIAL_RETRY_DELAY)

def read_serial():
    # Runs forever: reconnects whenever the port disappears or errors out,
    # instead of letting the exception kill the thread
    global serial_info_button

    while True:
        ser = open_serial()
        try:
            read_serial_lines(ser)
        except Exception as e:
            print(f"[Serial] Connection lost: {e}, reconnecting")
        finally:
            try:
                ser.close()
            except Exception:
                pass
        # Don't leave the button stuck "pressed" while disconnected
        serial_info_button = False
        time.sleep(SERIAL_RETRY_DELAY)

def read_serial_lines(ser):
    global serial_info_button, serial_brake, serial_clutch, serial_speed, serial_rpm

    buffer = ""
    last_line_time = time.time()
    while True:
        # Port still open but nothing arriving (e.g. Arduino hung): reconnect,
        # reopening the port also resets most Arduinos via DTR
        if time.time() - last_line_time > SERIAL_STALL_TIMEOUT:
            raise serial.SerialException(f"no data for {SERIAL_STALL_TIMEOUT}s")

        # Blocks up to the timeout instead of busy-looping
        byte = ser.read().decode(errors="ignore")
        if byte:
            if byte == '\n':
                last_line_time = time.time()
                line = buffer.strip()
                buffer = ''
                if line:
                    try:
                        if len(line) >= 6:  # Minimum size check
                            info_str   = line[-1]
                            brake_str  = line[-2]
                            clutch_str = line[-3]
                            rpm_str    = line[-7:-3]  # 4 chars before clutch/brake
                            speed_str  = line[:-7]    # everything else at the start

                            serial_speed  = float(speed_str)
                            serial_rpm    = int(rpm_str)
                            serial_clutch = (clutch_str == '1')
                            serial_brake  = (brake_str == '1')
                            serial_info_button = (info_str ==  '1')
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

# ADC DAC
adc = ADCDACPi(2)
adc.set_adc_refvoltage(3.3)

# GPIO

def GetThrottle() -> float:
    with adc_lock:
        return adc.read_adc_voltage(1, 0)

def SetThrottle(value):
    if value < 0:
        value = 0
    elif value > 3.29:
        value = 3.29

    with adc_lock:
        adc.set_dac_voltage(1, value)

last_throttle = 0
THROTTLE_IDLE_PERCENT = 7  # percentage shown with the pedal released
THROTTLE_SMOOTHING = 0.05  # EMA factor per call, lower = smoother

def GetThrottlePercentage() -> int:
    global last_throttle

    # Read raw throttle percentage from ADC
    with adc_lock:
        adc_voltage = adc.read_adc_voltage(1, 0)
    raw_value = (adc_voltage / 1.2 - 0.1) * 100

    # Pedal at rest reads ~THROTTLE_IDLE_PERCENT, remap so rest is 0% and full is 100%
    raw_value = (raw_value - THROTTLE_IDLE_PERCENT) / (100 - THROTTLE_IDLE_PERCENT) * 100
    raw_value = max(0, min(100, raw_value))  # Clamp to 0–100%

    # Apply exponential moving average
    last_throttle = last_throttle + THROTTLE_SMOOTHING * (raw_value - last_throttle)

    return int(round(last_throttle))

def GetClutch() -> bool:
    return serial_clutch

def GetBrake() -> bool:
    return serial_brake

gears = [137,77,53,42,28,25]
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

info_button = InfoButton()

def GetInfoButtonOnPressed():
    # short press, fires on release
    return info_button.short_pressed(serial_info_button)

def GetInfoButtonCruiseShortPressed():
    # short press as seen by the cruise thread
    return info_button.cruise_short_pressed(serial_info_button)

def GetInfoButtonLongPressed():
    # number of long press ticks (one per second held, first at the long press threshold)
    return info_button.long_ticks(serial_info_button)

def GetInfoButtonHeld():
    # True while the info button is down
    return info_button.held(serial_info_button)

def GetButtonPressed():
    return not GPIO.input(cruiseButtonPressed_pin)

def SetButtonLed(value):
    GPIO.output(cruiseButtonLed_pin, value)
