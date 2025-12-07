#!/usr/bin/python3

import sys
from Carviewer_dummy import *
import intro
import read
#import max7219
import threading

# Gets called once
def setup():
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
