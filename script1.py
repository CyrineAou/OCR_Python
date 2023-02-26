import cv2
import pytesseract
import re
import json

# Load the image
img = cv2.imread('img.png')

# Convert to grayscale and apply Gaussian blur
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)

# Initialize variables to hold class and attribute information
class_name = ''
attributes = []
output = []
class_data = []

# Apply OCR engine to extract text
text = pytesseract.image_to_string(blur)

# Parse the output to extract class names, attributes, and methods
class_names = re.findall(r'(?<=class\s)[a-zA-Z]+\w*', text)
attributes = re.fullmatch(r'^\s*[+-]\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*([a-zA-Z_][a-zA-Z0-9_]*(\[\])?)', text)
methods = re.findall(r'(?<=\n)[a-zA-Z]+\w*\s*\([a-zA-Z]*\)*\s*:\s*[a-zA-Z]+\w*', text)

# Build dictionary with extracted information
# If there is a class and attributes remaining, add them to the output list
if class_name != '':
    class_data.append({'class': class_name, 'attributes': attributes})

# Convert the list of classes to JSON format
json_data = json.dumps(class_data, indent=2)

# Print the JSON data
print(json_data)
