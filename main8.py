import pytesseract
from PIL import Image
import re

# Load the class diagram image
diagram = Image.open('class.png')

# Convert the image to grayscale
diagram = diagram.convert('L')

# Use Pytesseract to extract the text from the image
text = pytesseract.image_to_string(diagram)

# Define regular expression patterns for class name and attribute
class_pattern = r'class\s+(\w+)'
attribute_pattern = r'\s*(\w+)\s*:\s*(.*)'

# Search for the class name and attributes in the extracted text
match = re.search(class_pattern, text)
class_name = match.group(1) if match else None
attributes = []
for match in re.finditer(attribute_pattern, text):
    attributes.append((match.group(1), match.group(2)))

# Print the class name and attributes (or a message if not found)
if class_name is not None:
    print(f"Class name: {class_name}")
    for attribute in attributes:
        print(f"Attribute name: {attribute[0]}, value: {attribute[1]}")
else:
    print("Could not find class name in diagram")
