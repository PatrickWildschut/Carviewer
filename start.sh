#!/bin/bash

wlr-randr --output HDMI-A-1 --mode 1024x576

cd /home/fiesta/Carviewer
./main.py fullscreen
