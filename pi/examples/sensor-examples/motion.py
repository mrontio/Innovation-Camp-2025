from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(17)

while True:
    pir.wait_for_motion()
    print("Motion detected!")
    pir.wait_for_no_motion()
    print("Motion ended.")
