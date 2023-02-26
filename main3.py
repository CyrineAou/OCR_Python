import pytesseract
from PIL import Image
import io

# Open the PDF file as an image
with Image.open('class5.png') as img:

    # Convert the image to grayscale
    img = img.convert('L')

    # Convert the image to a byte stream
    img_byte = io.BytesIO()
    img.save(img_byte, format='PNG')
    img_byte.seek(0)

    # Perform OCR on the image
    text = pytesseract.image_to_string(Image.open(img_byte))

    # Print the extracted text
    print(text)