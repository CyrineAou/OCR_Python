import cv2
import pytesseract
import re


def remove_association_lines(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply OCR to recognize text in the image
    text = pytesseract.image_to_string(thresh, lang='eng')

    # Define a regular expression pattern that matches association lines and their associated text
    pattern = r'\s*([a-zA-Z0-9_]+)\s+--[o<>]+--\s+([a-zA-Z0-9_]+)\s*.*'

    # Search for the pattern in the text and replace it with an empty string
    modified_text = re.sub(pattern, '', text)

    # Return the modified text
    return modified_text

modified_text = remove_association_lines('img.png')
print(modified_text)
