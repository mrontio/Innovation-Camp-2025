from picamera2 import Picamera2
from PIL import Image
import numpy as np

picam2 = Picamera2()
picam2.start()
imgs = []

for _ in range(5):
    arr = picam2.capture_array()   # returns a NumPy array of shape (H, W, 3)
    imgs.append(arr)
images = np.stack(imgs)             # shape: (5, H, W, 3)
print(f"Image array shape: {images.shape}")

for i, arr in enumerate(images):
    img = Image.fromarray(arr)
    img.save(f'{i}.png')
