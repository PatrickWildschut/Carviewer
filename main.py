#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
from Carviewer_Arduino import *
import intro
import read
import cruise
#import max7219
import threading
import engine_off
import screensaver

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
    #thread = threading.Thread(target=SetMax7219Gear)
    #thread.start()

    # Cruise control runs in the background on every screen
    cruise.start_cruise_thread()

    # Start serial thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()

    engine_off.start(GetRPM)
    screensaver.start(GetSpeed)

    # NOTE: fullscreen is set up at startup by Carviewer_Arduino (based on the
    # "fullscreen" command line argument), so the screen surface stays valid.

    intro.show_intro()

# Main loop
def main():
    setup()

    read.read_menu()

#oldGear = -2
#def SetMax7219Gear():
#    global oldGear
#    while True:
#        currentGear = GetGear()
#
#        if currentGear != oldGear:
#            max7219.draw_gear(currentGear)
#            oldGear = currentGear
#
#        time.sleep(0.1)

if __name__ == "__main__":
    main()
