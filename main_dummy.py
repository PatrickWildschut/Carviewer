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

    # NOTE: fullscreen is set up at startup by Carviewer_dummy (based on the
    # "fullscreen" command line argument), so the screen surface stays valid.

    intro.show_intro()

# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
