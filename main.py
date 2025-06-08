#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
from Carviewer_global import *
import intro
import read

# Gets called once
def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # Setup pedals
    GPIO.setup(clutch_pin, GPIO.IN)
    GPIO.setup(brake_pin, GPIO.IN)
    GPIO.setup(cruiseButtonPressed_pin, GPIO.IN)

    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.setup(cruiseButtonLed_pin, GPIO.OUT)

    GPIO.setup(max7219_din, GPIO.OUT)
    GPIO.setup(max7219_cs, GPIO.OUT)
    GPIO.setup(max7219_clk, GPIO.OUT)

    SetButtonLed(True)
    SetRelays(False)

    if len(sys.argv) > 1:
        if sys.argv[1] == "fullscreen":
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    
    intro.show_intro()

# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
