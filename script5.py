import cv2
import pytesseract
import re

# Load the image
image = cv2.imread("class22.png")

# Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Define a regular expression pattern to match class names
class_name_pattern = r"class\s+(\w+)"

# Define a regular expression pattern to match attributes
attribute_pattern = r"(\w+)\s*:\s*(\w+)"

# Loop through the contours and extract text
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)

    # Extract the text from the bounding rectangle
    cropped = image[y:y+h, x:x+w]
    text = pytesseract.image_to_string(cropped)

    # Search for the class name using the regular expression pattern
    class_name_match = re.search(class_name_pattern, text)
    if class_name_match:
        class_name = class_name_match.group(1)
        print(f"Class name: {class_name}")

        # Search for attributes using the regular expression pattern
        attribute_matches = re.findall(attribute_pattern, text)
        for attribute_match in attribute_matches:
            attribute_name = attribute_match[0]
            attribute_type = attribute_match[1]
            print(f"Attribute: {attribute_name}, Type: {attribute_type}")
