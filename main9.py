import cv2
import pytesseract
import json

# Load the UML class diagram image using OpenCV
img = cv2.imread('class.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Initialize variables to hold class and attribute information
classes = []

# Iterate over each contour
for contour in contours:
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)
    # Check if the contour has the aspect ratio of a UML class box
    aspect_ratio = float(w) / h
    if aspect_ratio > 1.5 and aspect_ratio < 3.0:
        # Extract the text from the contour using Tesseract OCR
        class_name = pytesseract.image_to_string(gray[y:y+h, x:x+w], lang='eng', config='--psm 6')
        class_name = class_name.strip()
        # Initialize variables to hold attribute information
        attributes = []
        # Iterate over each child contour of the current contour
        child_contours = hierarchy[0][hierarchy[0][:, 3] == contour[0][3]]
        for child_contour in child_contours:
            # Get the bounding rectangle of the child contour
            cx, cy, cw, ch = cv2.boundingRect(child_contour)
            # Check if the child contour has the aspect ratio of a UML attribute box
            child_aspect_ratio = float(cw) / ch
            if child_aspect_ratio > 1.5 and child_aspect_ratio < 3.0:
                # Extract the text from the child contour using Tesseract OCR
                attribute_name = pytesseract.image_to_string(gray[cy:cy+ch, cx:cx+cw], lang='eng', config='--psm 6')
                attribute_name = attribute_name.strip()
                # Extract the attribute type from the text
                attribute_type = ''
                if ':' in attribute_name:
                    attribute_name, attribute_type = attribute_name.split(':', 1)
                    attribute_type = attribute_type.strip()
                # Add the attribute to the list of attributes
                attributes.append({'name': attribute_name, 'type': attribute_type})
        # Add the class and its attributes to the list of classes
        classes.append({'name': class_name, 'attributes': attributes})

# Convert the list of classes to JSON format
json_data = json.dumps(classes, indent=2)

# Print the JSON data
print(json_data)
