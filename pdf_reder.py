import pytesseract
import json
import re
from PIL import ImageFilter
from pdf2image import convert_from_path

# Path to PDF file
pdf_file = 'png2pdf.pdf'

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
        match_class = re.match(r'class\s+(\w+)(?:\s*\(\s*\w+\s*\))?(?:\s+extends\s+\w+)?(?:\s+implements\s+\w+(?:\s*,\s*\w+)*)?(?:\s*\{\s*)?', line, re.IGNORECASE)
        if match_class:
            # Found class name
            class_name = match_class.group(1)
            # Found attributes
            attributes = [{'name': attr.group(1).strip(), 'type': attr.group(2).strip()} for attr in re.finditer(r'(\w+)\s*:\s*(\w+)', page_text)]
            # Add class data to JSON output
            class_data[f'page{i + 1}'] = {'class_name': class_name, 'attributes': attributes}

# Output class data as JSON
output = {'attributes': class_data}
json_output = json.dumps(output, indent=2, sort_keys=True)

print(json_output)
