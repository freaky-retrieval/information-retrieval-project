from PIL import Image
import numpy as np

def test_loading():
    for i in range(2):
        print("Loading...")


blank_image = np.ones((200, 700, 4), dtype=np.uint8) * 255
diffusion_image = Image.fromarray(blank_image, "RGBA")