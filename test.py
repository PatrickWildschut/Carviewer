import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.OUT)

while True:
        GPIO.output(40, GPIO.LOW)
        time.sleep(0.05)