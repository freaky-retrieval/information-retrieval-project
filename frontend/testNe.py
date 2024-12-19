from PIL import Image
import numpy as np
from transformers import pipeline

def sentiment_analysis(text):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased")
    result = classifier(text)
    return result

def test_loading():
    for i in range(2):
        (sentiment_analysis("I am a cat"))


blank_image = np.ones((200, 700, 4), dtype=np.uint8) * 255
diffusion_image = Image.fromarray(blank_image, "RGBA")