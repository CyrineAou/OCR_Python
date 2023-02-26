import re
import sys
import pyocr
import pyocr.builders
from PIL import Image

# Define regular expressions for matching class, attribute, and method information
class_regex = re.compile(r'^[A-Z][a-zA-Z0-9_]{2,}\s*(<\s*[A-Z][a-zA-Z0-9_]+\s*>)?$')
attribute_regex = re.compile(r'^\s*([+-])\s*([a-zA-Z_][a-zA-Z0-9_]*|\n)\s*\((.*)\)\s*:\s*(.*)$')
method_regex = re.compile(r'^\s*([+-])\s*([a-zA-Z_][a-zA-Z0-9_]*|\n)\s*\((.*)\)\s*->\s*(.*)$')

# Initialize variables to hold class and attribute information
class_name = ''
attributes = []
methods = []
output = []

# Initialize OCR engine
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
else:
    tool = tools[0]

# Load the class diagram image using PIL
image = Image.open('class22.png')

# Extract text from the image using OCR
text = tool.image_to_string(
    image,
    lang='eng',
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
)

# Split the text into lines
lines = text.split('\n')

# Define a lambda expression to remove association information
remove_association = lambda l: re.sub(r'\s*--\s*.*\s*$', '', l)

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