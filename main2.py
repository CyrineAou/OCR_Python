import pytesseract
from PIL import Image

# Load the class diagram image
diagram = Image.open('class.png')

# Convert the image to grayscale
diagram = diagram.convert('L')

# Use Pytesseract to extract the text from the image
text = pytesseract.image_to_string(diagram)

# Search for the attribute you're interested in
attribute_name = 'my_attribute'
attribute_value = None

# Split the text into lines and search for the attribute name
for line in text.split('\n'):
    if attribute_name in line:
        # If the attribute name is found, extract the attribute value
        attribute_value = line.split(attribute_name)[1].strip()
        break

# Print the attribute value (or a message if the attribute was not found)
if attribute_value is not None:
    print(f"The value of {attribute_name} is {attribute_value}")
else:
    print(f"Could not find attribute {attribute_name}")
