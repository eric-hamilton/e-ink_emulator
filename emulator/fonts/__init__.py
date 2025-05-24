from PIL import ImageFont
import os

def create_font(font_name, font_size):
    """
    Takes a TTF font filename and a font size, returns an ImageFont instance.
    Ex: create_font("TimeMono.ttf", 64)
    """
    font_dir = os.path.dirname(__file__)
    font_path = os.path.join(font_dir, font_name)
    return ImageFont.truetype(font_path, font_size)
