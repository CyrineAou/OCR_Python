import pytesseract
import json
import re
from PIL import ImageFilter
from pdf2image import convert_from_path

# Path to PDF file
pdf_file = 'classpdf.pdf'

# Convert PDF to image
pages = convert_from_path(pdf_file)

# Extract text from each page using OCR
text = []
for page in pages:
    # Apply image processing to enhance OCR accuracy
    processed_image = page.filter(ImageFilter.SHARPEN).convert('L')
    text.append(pytesseract.image_to_string(processed_image))

# Parse class diagram text into JSON format
class_data = {}
for i, page_text in enumerate(text):
    # Look for lines of text that contain class name and attributes
    lines = page_text.strip().split('\n')
    class_name = None
    attributes = []
    for line in lines:
        # Use regular expression to find class name and attributes
        match_class = re.match(r'class\s+(\w+)', line, re.I)
        match_attr = re.match(r'(\w+)\s*:\s*(\w+)', line)
        if match_class:
            # Found class name
            class_name = match_class.group(1)
        elif match_attr:
            # Found attribute
            attribute_name, attribute_type = match_attr.groups()
            attributes.append({'name': attribute_name, 'type': attribute_type})
    # Add class data to JSON output
    if class_name:
        class_data[f'page{i+1}'] = {'class_name': class_name, 'attributes': attributes}

# Output class data as JSON
output = {'class_data': class_data}
json_output = json.dumps(output, indent=2, sort_keys=True)

print(json_output)
