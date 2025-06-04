import pygame
import sys
from picamera2 import Picamera2
from PIL import Image
import numpy as np
import spidev
import time

picam2 = Picamera2()
spi = spidev.SpiDev()

WATER_LEVEL_CHANNEL = 0

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

# Execution begins here
if not init_sensors():
    print(f'error: sensor initialisation failed')
    sys.exit(1)

# Interesting part begins here

try:
    while True:
        water_level = read_analog_channel(WATER_LEVEL_CHANNEL)
        print(water_level)
        if (water_level >= 200):
            play_audio('slurp.wav')

        if (water_level <= 10):
            play_audio('water.wav')

        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl-C Pressed.")
