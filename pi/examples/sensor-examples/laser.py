import RPi.GPIO as GPIO
import time

LASER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

# Turn on laser
yeah = True
for i in range(1000):
    yeah = not yeah
    GPIO.output(LASER_PIN, yeah)
    time.sleep(.1)

# for i in range(20):
#     yeah = not yeah
#     GPIO.output(LASER_PIN, yeah)
#     time.sleep(.3)

# Turn off laser
GPIO.output(LASER_PIN, False)

GPIO.cleanup()
