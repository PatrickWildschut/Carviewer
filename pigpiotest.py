import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon")
    exit()

# GPIO pin 32
pin = 13

# Set the pin to input mode
pi.set_mode(pin, pigpio.INPUT)

def pwm_callback(gpio, level, tick):
    global last_tick, high_tick, period
    if level == 1:
        if last_tick is not None:
            period = pigpio.tickDiff(last_tick, tick)
        last_tick = tick
    elif level == 0:
        if last_tick is not None:
            high_tick = pigpio.tickDiff(last_tick, tick)

last_tick = None
high_tick = None
period = None

cb = pi.callback(pin, pigpio.EITHER_EDGE, pwm_callback)

try:
    while True:
        if period is not None and high_tick is not None:
            frequency = 1000000 / period
            duty_cycle = (high_tick / period) * 100
            print(frequency * 0.73)
        else:
            print(-1)
        time.sleep(1)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Exiting...")
finally:
    cb.cancel()
    pi.stop()  # Clean up and stop the pigpio daemon
