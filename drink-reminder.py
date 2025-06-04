import pygame
import sys
from picamera2 import Picamera2
from PIL import Image
import numpy as np

picam2 = Picamera2()

def init_sensors() -> bool:
    '''
    Initialise the sensors for our project.
    The current list is:
    - Speaker via pygame
    '''

    pygame.mixer.init()
    picam2.start()
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

# Execution begins here
if not init_sensors():
    print(f'error: sensor initialisation failed')
    sys.exit(1)

#play_audio('example.wav')
img_np = capture_image_np(picam2)
print(f"Image array shape: {img_np.shape}")
save_image_np(img_np, './cam.png')

for channel in range(img_np.shape[2]):
    print(f"Channel {channel} avg: {img_np[:,:,channel].mean()}")

if img_np[:,:,channel].mean() > 250:
    play_audio('red.wav')
