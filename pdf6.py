import cv2
import pytesseract
import re
import json
import numpy as np
from pdf2image import convert_from_path

def detect_class_data(text):
    # Refine the regular expressions to extract class name and attributes
    class_name_pattern = r'class\s+(\w+)\s*(?:\{\s*|\n)'
    class_name_match = re.search(class_name_pattern, text)

    attribute_pattern = r'(\w[\w\s]*?)\s*:\s*(\w[\w\s]*?)\s*(?=[\n}])'
    attribute_matches = re.findall(attribute_pattern, text)

    # Create a dictionary to store the output for this page
    page_output = {
        'class_name': class_name_match.group(1).strip() if class_name_match else None,
        'attributes': [{'name': match[0].strip(), 'type': match[1].strip()} for match in attribute_matches]
    }

    # Calculate the degree of precision
    degree_of_precision = len(text) / (len(text) + text.count(' '))

    # Add the degree of precision to the output dictionary
    page_output['degree_of_precision'] = degree_of_precision

    return page_output


def extract_class_data_from_image(image_path):
    # Load the class diagram image using OpenCV
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

    # Split the modified text into pages based on the 'class' keyword
    pages = re.split(r'\bclass\b', modified_text)[1:]

    # Process each page of the text
    class_data = []
    for page in pages:
        # Extract class data from the page
        page_data = detect_class_data(page)

        # Add the output for this page to the list of class data
        class_data.append(page_data)

    # Output class data as JSON
    output = {'class_data': class_data}
    json_output = json.dumps(output, indent=2, sort_keys=True)

    return json_output
