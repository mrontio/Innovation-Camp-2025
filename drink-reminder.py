import pygame
import sys
from picamera2 import Picamera2
from PIL import Image
import numpy as np
import spidev
import time
from rpi_lcd import LCD
import RPi.GPIO as GPIO

picam2 = Picamera2()
spi = spidev.SpiDev()
lcd = LCD()

WATER_LEVEL_CHANNEL = 0
R_LED = 22
G_LED = 27
B_LED = 17

def init_sensors() -> bool:
    '''
    Initialise the sensors for our project.
    The current list is:
    - Speaker via pygame
    '''

    pygame.mixer.init()
    picam2.start()
    spi.open(0, 0)            # bus 0, device 0 (CE0)
    spi.max_speed_hz = 1350000
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(R_LED, GPIO.OUT)
    GPIO.setup(G_LED, GPIO.OUT)
    GPIO.setup(B_LED, GPIO.OUT)

    return True

def play_audio(wav_file: str):
    '''
    Play the audio file provided in `wav_file`.
    Must be a path.
    '''
    pygame.mixer.music.load(wav_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

def capture_image_np(cam: Picamera2) -> np.ndarray:
    return picam2.capture_array()

def save_image_np(img_np: np.ndarray, path: str) -> None:
    img = Image.fromarray(img_np)
    img.save(path)

def read_analog_channel(channel):
    # send start bit, single-ended mode, channel (ch 0–7)
    command = 0b11 << 6 | (channel & 0x07) << 3
    response = spi.xfer2([command, 0, 0])
    return ((response[0] & 1) << 9) | (response[1] << 1) | (response[2] >> 7)

def print_to_lcd(line1: str, line2: str, lcd: LCD):
    if len(line1) > 15 or len(line2) > 15:
        print('warning: text exceeds 15 characters will not be rendered.')
    lcd.text(line1, 1)
    lcd.text(line2, 2)

def show_led_colour(r: bool, g: bool, b: bool) -> None:
    GPIO.output(R_LED, r)
    GPIO.output(G_LED, g)
    GPIO.output(B_LED, b)

def cup_detected(img_np: np.ndarray, detection_threshold=200_000_000) -> bool:
    return img_np.sum() > detection_threshold

def get_sensor_into_cup(lcd):
    print_to_lcd("    I THIRST   ", "    FOR MORE   ", lcd)
    while read_analog_channel(WATER_LEVEL_CHANNEL) < 20:
        play_audio('water.wav')
    lcd.clear()
    return

def remind_user_about_water(lcd):
    print_to_lcd("    CONSUME    ", "     WATER     ", lcd)
    image_np = capture_image_np(picam2)
    while cup_detected(image_np):
        image_np = capture_image_np(picam2)
        print(image_np.sum(), cup_detected(image_np))
        play_audio('slurp.wav')
    lcd.clear()
    return


def cleanup():
    lcd.clear()


# Execution begins here
if not init_sensors():
    print(f'error: sensor initialisation failed')
    sys.exit(1)

##### Interesting part begins here #####

# Control Variables
tick_length_s = 1.0
ticks_till_reminder = 5
lcd_second_line = ""

# Try catch statement (so we can press Ctrl-C easily)
try:
    while True:
        ticks_till_reminder -= 1
        water_level = read_analog_channel(WATER_LEVEL_CHANNEL)
        image_np = capture_image_np(picam2)
        print(f"ticks left: {ticks_till_reminder}, image sum: {image_np.sum()}, water_level: {water_level}")
        if cup_detected(capture_image_np(picam2)):
            # Cup has been detected
            if water_level < 20:
                # Sensor not in cup / cup empty, politely remind.
                show_led_colour(r=False, g=False, b=True)
                get_sensor_into_cup(lcd)
            elif ticks_till_reminder < 1:
                # Sensor is back in cup, and the timer is done. Remind the user.
                show_led_colour(r=False, g=True, b=False)
                print("hi?")
                remind_user_about_water(lcd)
                ticks_till_reminder = 10
        else:
            show_led_colour(r=True, g=False, b=False)

        time.sleep(tick_length_s)

except KeyboardInterrupt:
    print("Ctrl-C Pressed.")

cleanup()
