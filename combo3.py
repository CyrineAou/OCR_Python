import pytesseract
import re
import cv2
# Load the image using a library like OpenCV
img = cv2.imread('img.png')

# Use an OCR tool like Tesseract to extract text from the image
text = pytesseract.image_to_string(img)

# Create a dictionary of keywords to identify classes, attributes, and methods
class_dict = {'class': ['\bclass\b'],
              'attribute': ['\battribute\b', '\battr\b'],
              'method': ['\bmethod\b']}

# Create a regular expression to extract the name of the class
class_regex = re.compile('\bclass\s+(\w+)')

# Create regular expressions to extract the name and type of an attribute
attr_name_regex = re.compile('\battribute\s+(\w+)\b')
attr_type_regex = re.compile('\b(\w+)\s+attribute\b')

# Create regular expressions to extract the name, return type, and parameters of a method
method_name_regex = re.compile('\bmethod\s+(\w+)\b')
return_type_regex = re.compile('\b(\w+)\s+method\b')
param_regex = re.compile('\((.*?)\)')

# Initialize empty lists to store the class, attribute, and method names
classes = []
attributes = []
methods = []

# Loop through each line of text in the OCR output
for line in text.split('\n'):
    # Check if the line matches the pattern for a class
    class_match = class_regex.match(line)
    if class_match:
        class_name = class_match.group(1)
        classes.append(class_name)

    # Check if the line matches the pattern for an attribute
    for keyword in class_dict['attribute']:
        if keyword in line and class_regex.search(line):
            attr_name_match = attr_name_regex.search(line)
            attr_type_match = attr_type_regex.search(line)
            if attr_name_match and attr_type_match:
                attribute_name = attr_name_match.group(1)
                attribute_type = attr_type_match.group(1)
                attributes.append((attribute_name, attribute_type))

    # Check if the line matches the pattern for a method
    for keyword in class_dict['method']:
        if keyword in line and class_regex.search(line):
            method_name_match = method_name_regex.search(line)
            return_type_match = return_type_regex.search(line)
            param_match = param_regex.search(line)
            if method_name_match and return_type_match:
                method_name = method_name_match.group(1)
                return_type = return_type_match.group(1)
                if param_match:
                    params = param_match.group(1)
                else:
                    params = ''
                methods.append((method_name, return_type, params))

# Print the extracted class, attribute, and method names
print(classes)
print(attributes)
print(methods)
