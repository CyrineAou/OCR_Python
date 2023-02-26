import cv2
import pytesseract
import re

# Load the class diagram image using OpenCV
img = cv2.imread('class.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply OCR to recognize text in the image
text = pytesseract.image_to_string(thresh, lang="eng")

# Split the text into lines
lines = text.split('\n')

# Define regular expressions for matching class, attribute, and method information
class_regex = re.compile(r'^[A-Z][a-zA-Z0-9_]{2,}\s*(<\s*[A-Z][a-zA-Z0-9_]+\s*>)?$')
attribute_regex = re.compile(r'^\s*([+-])\s*([a-zA-Z_][a-zA-Z0-9_]*|\n)\s*\((.*)\)\s*:\s*(.*)$')
method_regex = re.compile(r'^\s*([+-])\s*([a-zA-Z_][a-zA-Z0-9_]*|\n)\s*\((.*)\)\s*->\s*(.*)$')

# Define a lambda expression to remove association information
remove_association = lambda l: re.sub(r'\s*--\s*.*\s*$', '', l)

# Initialize variables to hold class and attribute information
class_name = ''
attributes = []
methods = []
output = []

# Iterate over each line
for line in lines:
    # Remove association information from the line
    line = remove_association(line.strip())
    # Check if the line matches the pattern for a class name
    if class_regex.match(line):
        # If we've already processed a class, add its attributes and methods to the output list
        if class_name != '':
            # Format the class, its attributes, and its methods
            output.append({'class': class_name, 'attributes': attributes, 'methods': methods})
            # Reset the attributes and methods lists
            attributes = []
            methods = []
        # Store the name of the current class
        class_name = line
    else:
        # Check if the line matches the pattern for an attribute or a method
        attribute_match = attribute_regex.match(line)
        method_match = method_regex.match(line)
        if attribute_match:
            # Store the visibility, name, arguments, and return type of the attribute
            groups = attribute_match.groups()
            if len(groups) >= 4:
                visibility, name, arguments, return_type = groups[:4]
                attributes.append({'visibility': visibility.strip(), 'name': name.strip(), 'type': return_type.strip()})
        elif method_match:
            # Store the visibility, name, arguments, and return type of the method
            groups = method_match.groups()
            if len(groups) >= 4:
                visibility, name, arguments, return_type = groups[:4]
            methods.append({'visibility': visibility.strip(), 'name': name.strip(), 'arguments': arguments.strip(),
                            'return_type': return_type.strip()})

    # If we have processed at least one class, add its attributes and methods to the output list
    if class_name != '':
        # Format the class, its attributes, and its methods
        output.append({'class': class_name, 'attributes': attributes, 'methods': methods})

        # Print the output
    print(output)