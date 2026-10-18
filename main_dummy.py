#!/usr/bin/python3

import sys
# Local testing: stand in for the Raspberry Pi specific Carviewer_Arduino
import Carviewer_dummy
sys.modules['Carviewer_Arduino'] = Carviewer_dummy

from Carviewer_Arduino import *
import intro
import read
import cruise
import layouts
#import max7219
import threading
import os
import time
import pygame
import engine_off
import screensaver

# Key legend, only shown on the original layout so it's clear what the keys do.
KEY_HINTS = [
    "[I]  Info button (tap / hold)",
    "[R]  Hold: engine off (RPM 0)",
    "[S]  Screensaver",
]
HINT_COLOR = (130, 130, 145)
original_dashboard = layouts.original_dashboard
def original_dashboard_with_hints(*args, **kwargs):
    original_dashboard(*args, **kwargs)
    hint_font = pygame.font.Font(None, S(22))
    for i, hint in enumerate(KEY_HINTS):
        screen.blit(hint_font.render(hint, True, HINT_COLOR), (S(570), S(40) + i * S(22)))
layouts.original_dashboard = original_dashboard_with_hints

# Gets called once
def setup():
    SetButtonLed(True)
    SetRelays(False)

    cruise.start_cruise_thread()

    # Hold R to set RPM to 0. Shutting down is simulated: just quit the program.
    def fake_shutdown():
        print("shutdown now (dummy)")
        os._exit(0)
    engine_off.start(GetRPM, fake_shutdown)

    # Press S to start the screensaver. Normally it starts after 1 minute at speed 0.
    screensaver.start(GetSpeed)
    def watch_s_key():
        was_pressed = False
        while True:
            pressed = pygame.key.get_pressed()[pygame.K_s]
            if pressed and not was_pressed:
                screensaver.activate()
            was_pressed = pressed
            time.sleep(0.05)
    threading.Thread(target=watch_s_key, daemon=True).start()

    # NOTE: fullscreen is set up at startup by Carviewer_dummy (based on the
    # "fullscreen" command line argument), so the screen surface stays valid.

    intro.show_intro()

# Main loop
def main():
    setup()

    read.read_menu()

if __name__ == "__main__":
    main()
