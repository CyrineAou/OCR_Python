import pytesseract
import json
import cv2
import numpy as np
from pdf2image import convert_from_path
import re

def detect_text(pdf_path):
    # Convert the PDF file to a list of PIL images
    pages = convert_from_path(pdf_path)

    # Set the path to the Tesseract OCR executable file
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Create an empty list to store the class data for each page
    class_data = []

    # Process each page of the PDF file
    for i, page in enumerate(pages):
        # Convert the PIL image to a NumPy array
        image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # Resize the image to improve OCR accuracy
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Apply contrast stretching
        p2, p98 = np.percentile(image, (2, 98))
        image = np.uint8(np.clip((image - p2) / (p98 - p2) * 255.0, 0, 255))

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Apply edge detection
        edges = cv2.Canny(thresh, 100, 200)

        # Pass the preprocessed image to the Tesseract OCR engine
        text = pytesseract.image_to_string(edges, lang='eng', config='--psm 6')

        # Refine the regular expressions to extract class name and attributes
        class_name_pattern = r'^\s*[+-]\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*([a-zA-Z_][a-zA-Z0-9_]*(\[\])?)'
        class_name_match = re.search(class_name_pattern, text)

        attribute_pattern = r'(\w[\w\s]*?)\s*:\s*(\w[\w\s]*?)\s*(?=[\n}])'
        attribute_matches = re.findall(attribute_pattern, text)

        # Create a dictionary to store the output for this page
        page_output = {
            'class_name': class_name_match.group(1).strip() if class_name_match else None,
            'attributes': [{'name': match[0].strip(), 'type': match[1].strip()} for match in attribute_matches]
        }

        # Calculate the degree of precision
        degree_of_precision = len(text) / (image.shape[0] * image.shape[1])

        # Add the degree of precision to the output dictionary
        page_output['degree_of_precision'] = degree_of_precision

        # Add the output for this page to the list of class data
        class_data.append(page_output)

    return class_data


# Path to PDF file
pdf_file = 'png2pdf.pdf'

# Extract text from each page using OCR
class_data = detect_text(pdf_file)

# Output class data as JSON
output = {'class_data': class_data}
json_output = json.dumps(output, indent=2, sort_keys=True)

print(json_output)
