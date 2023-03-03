import cv2
import numpy
import pytesseract
import json
import re
from pdf2image import convert_from_path

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
        image = cv2.cvtColor(numpy.array(page), cv2.COLOR_RGB2BGR)

        # Resize the image to improve OCR accuracy
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to convert it into a binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply noise removal techniques to remove noise from the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # Pass the preprocessed image to the Tesseract OCR engine
        text = pytesseract.image_to_string(opening)

        # Search for patterns using regular expressions
        class_name_pattern = r'class\s.*\n\s*(\w+)'
        class_name_match = re.search(class_name_pattern, text)

        attribute_pattern = r'(\w+)\s*:\s*(\w+)'
        attribute_matches = re.findall(attribute_pattern, text)

        # Create a dictionary to store the output for this page
        page_output = {
            'class_name': class_name_match.group(1) if class_name_match else None,
            'attributes': [{'name': match[0], 'type': match[1]} for match in attribute_matches]
        }

        # Calculate the degree of precision
        degree_of_precision = len(text) / (image.shape[0] * image.shape[1])

        # Add the degree of precision to the output dictionary
        page_output['degree_of_precision'] = degree_of_precision

        # Add the output for this page to the list of class data
        class_data.append(page_output)

    # Create a dictionary to store the output for all pages
    output = {'attributes': class_data}

    # Convert the dictionary to JSON format
    json_output = json.dumps(output)

    return json_output

# Call the detect_text function with the path to the PDF file
json_output = detect_text('classpdf.pdf')

# Print the JSON output
print(json_output)
