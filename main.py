#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys

from Carviewer_global import *
import read

# Gets called once
def setup():
    GPIO.setmode(GPIO.BOARD)

    # Setup pedals
    GPIO.setup(clutch_pin, GPIO.IN)
    GPIO.setup(brake_pin, GPIO.IN)
    GPIO.setup(cruiseButtonPressed_pin, GPIO.IN)

    GPIO.setup(relay1_pin, GPIO.OUT)
    GPIO.setup(relay2_pin, GPIO.OUT)
    GPIO.setup(cruiseButtonLed_pin, GPIO.OUT)

    SetButtonLed(True)

# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
