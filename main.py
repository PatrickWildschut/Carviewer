#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
from Carviewer_ESP32 import *
import intro
import read
import max7219
import threading

# Gets called once
def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # Setup pedals
    #GPIO.setup(clutch_pin, GPIO.IN)
    #GPIO.setup(brake_pin, GPIO.IN)
    GPIO.setup(cruiseButtonPressed_pin, GPIO.IN)

    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.setup(cruiseButtonLed_pin, GPIO.OUT)

    GPIO.setup(max7219_din, GPIO.OUT)
    GPIO.setup(max7219_cs, GPIO.OUT)
    GPIO.setup(max7219_clk, GPIO.OUT)

    SetButtonLed(True)
    SetRelays(False)

    # MAX7219 gear background update
    thread = threading.Thread(target=SetMax7219Gear)
    thread.start()

    # Start serial thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()

    if len(sys.argv) > 1:
        if sys.argv[1] == "fullscreen":
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    
    intro.show_intro()

# Main loop
def main():
    setup()

    read.read_menu()

oldGear = -2
def SetMax7219Gear():
    global oldGear
    while True:
        currentGear = GetGear()

        if currentGear != oldGear:
            max7219.draw_gear(currentGear)
            oldGear = currentGear

        time.sleep(0.1)

if __name__ == "__main__":
    main()
