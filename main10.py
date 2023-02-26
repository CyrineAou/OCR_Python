import pytesseract
import cv2
import re
import json

# Load the image of the class diagram
img = cv2.imread('class.png')

# Use Tesseract OCR to recognize the text in the image
text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')

# Define regular expressions to extract the names of classes, attributes, and methods
class_regex = r'class\s+(\w+)\s*\{'
attribute_regex = r'\s*(\w+)\s*:\s*(\w+)\s*'
method_regex = r'\s*(\w+)\s*\(\s*\)\s*:\s*(\w+)\s*'

# Search for matches of the regular expressions in the text string
class_matches = re.findall(class_regex, text)
attribute_matches = re.findall(attribute_regex, text)
method_matches = re.findall(method_regex, text)

# Create a dictionary to store the extracted information
result = {
    "Classes": class_matches,
    "Attributes": attribute_matches,
    "Methods": method_matches
}

# Convert the dictionary to a JSON string
json_str = json.dumps(result, indent=4)

# Print the JSON string
print(json_str)
