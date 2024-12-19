from streamlit_drawable_canvas import st_canvas
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


diffusion_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        update_streamlit=True,
        height=200,
        width=700,
        drawing_mode="freedraw",
        key="canvas",
    )

blank_image = np.ones((200, 700, 4), dtype=np.uint8) * 255
diffusion_image = Image.fromarray(blank_image, "RGBA")