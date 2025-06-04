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


def show_led_colour(r: bool, g: bool, b: bool):
    GPIO.output(R_LED, r)
    GPIO.output(G_LED, g)
    GPIO.output(B_LED, b)

def cleanup():
    lcd.clear()


# Execution begins here
if not init_sensors():
    print(f'error: sensor initialisation failed')
    sys.exit(1)

# Interesting part begins here
try:
    while True:
        water_level = read_analog_channel(WATER_LEVEL_CHANNEL)
        print_to_lcd("Water level:", str(water_level), lcd)

        image_np = capture_image_np(picam2)
        dominant_colour = np.argmax(np.mean(image_np[:,:,:3], axis=(0, 1))).item()
        show_led_colour(dominant_colour == 0, dominant_colour == 1, dominant_colour == 2)

        if (water_level >= 200):
            play_audio('slurp.wav')

        if (water_level <= 10):
            play_audio('water.wav')



        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl-C Pressed.")

cleanup()
