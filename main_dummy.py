#!/usr/bin/python3

import sys
# Local testing: stand in for the Raspberry Pi specific Carviewer_Arduino
import Carviewer_dummy
sys.modules['Carviewer_Arduino'] = Carviewer_dummy

from Carviewer_Arduino import *
import intro
import read
import cruise
#import max7219
import threading

# Gets called once
def setup():
    SetButtonLed(True)
    SetRelays(False)

    cruise.start_cruise_thread()

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
