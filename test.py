import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

while True:
        time.sleep(1)
        print(GPIO.input(11))