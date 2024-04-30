import pygame
import RPi.GPIO as GPIO

from Carviewer_global import *
import read

settings_json = None

# Gets called once
def setup():
    GPIO.setmode(GPIO.BOARD)

    settings_json = load_json()

    # Setup pedals
    GPIO.setup(settings_json["GPIO"]["clutch"], GPIO.IN)
    GPIO.setup(settings_json["GPIO"]["brake"], GPIO.IN)
    GPIO.setup(settings_json["GPIO"]["speed"], GPIO.IN)


# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
