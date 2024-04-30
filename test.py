from ADCDACPi import ADCDACPi
import time

adc = ADCDACPi(1)

adc.set_adc_refvoltage(3.3)

while True:

        # read the voltage from channel 1 in single-ended mode
        # and display on the screen

        print(adc.read_adc_voltage(1, 0))

        time.sleep(0.1)