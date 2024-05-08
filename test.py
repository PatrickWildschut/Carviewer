import RPi.GPIO as GPIO
import time
import pywinctl as pwc

window = pwc.getAllWindows()

print(window)