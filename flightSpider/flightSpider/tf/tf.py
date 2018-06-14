import os

from PIL import Image
import tesserocr
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
if __name__ == '__main__':
    p1 = Image.open('1.png')
    tesserocr.image_to_text(p1)
