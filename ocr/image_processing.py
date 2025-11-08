import cv2
import numpy as np
import pytesseract
import re
from collections import Counter

def clean_text(input_text):
    input_text = input_text.replace('\n', ' ')
    input_text = re.sub(r'\s+', ' ', input_text).strip() # replace trailing white spaces and make the one each
    input_text = input_text.lower()
    
    return input_text

def do_scaling(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    heights = data['height']
    texts = data['text']
    h = [height for text, height in zip(texts, heights) if text.strip() and height > 0] # filter out only recognized text boxes
    h = Counter(h).most_common(1)[0][0] # get the height with the most occurences
    scaling_factor = round(30 / h, 2) # calculate factor to gain font size 30
    image = cv2.resize(image, None, fx = scaling_factor, fy = scaling_factor, interpolation = cv2.INTER_LANCZOS4)
    
    return image

def do_invertion(image):
    white = np.sum(image == 255)
    black = np.sum(image == 0)
    if black > white:
        image = 255 - image # invert image only if black value is higher than whites
        
    return image

def process_image(contents, config):
    nparr = np.frombuffer(contents, np.uint8) # convert with numpy to read with opencv
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE) # read with grayscale conversion
    
    image = do_scaling(image)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    image = do_invertion(image)
    image = cv2.GaussianBlur(image, (3,3), 0)
    # add white border of 10 pixels to image
    image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    text = pytesseract.image_to_string(image, config=config)
    text = clean_text(text)

    return text
