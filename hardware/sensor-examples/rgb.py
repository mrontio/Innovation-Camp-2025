import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
for p in (17, 27, 22):
    GPIO.setup(p, GPIO.OUT)

# red = on, green & blue = off
GPIO.output(17, False)
GPIO.output(27, True)
GPIO.output(22, 100)

import time
time.sleep(5)
