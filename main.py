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
    

# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
