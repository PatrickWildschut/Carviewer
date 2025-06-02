import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN)

while True:
    time.sleep(0.2)
    print(GPIO.input(36))