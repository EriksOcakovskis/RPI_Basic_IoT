# import Raspberry Pi GPIO support into Python environment
import RPi.GPIO as GPIO
# import a sleep function from time module
from time import sleep

ledR = 10  # GPIO number where the led is connected
ledB = 27
ledG = 22

# Tell the GPIO module to use GPIO numbering used by processor
GPIO.setmode(GPIO.BCM)

# Set GPIO no 18 to output mode
GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)
GPIO.setup(ledG, GPIO.OUT)

# Blink some leds
while True:
    GPIO.output(ledR, False)
    sleep(1)  # Sleep for 1 second
    GPIO.output(ledR, True)
    GPIO.output(ledB, False)
    sleep(1)
    GPIO.output(ledB, True)
    GPIO.output(ledG, False)
    sleep(1)
    GPIO.output(ledG, True)
