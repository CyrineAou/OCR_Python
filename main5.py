import PyPDF2
import pytesseract
import cv2

# Open the PDF file
pdf_file = open('class.png')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Select the page with the class diagram
page = pdf_reader.getPage(0)

# Convert the PDF page to an image
dpi = 300
scale_percent = 100
width = int(page.mediaBox.getWidth() * dpi / 72 * scale_percent / 100)
height = int(page.mediaBox.getHeight() * dpi / 72 * scale_percent / 100)
image = cv2.imread(page, cv2.IMREAD_COLOR)

# Define the area containing the cardinality text
x, y, w, h = 100, 200, 200, 50
roi = image[y:y+h, x:x+w]

# Preprocess the image to improve OCR accuracy
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform OCR on the preprocessed image
cardinality_text = pytesseract.image_to_string(blur)

# Extract the cardinality information from the OCR result
cardinality = ''
if '0..*' in cardinality_text:
    cardinality = '0..*'
elif '0..1' in cardinality_text:
    cardinality = '0..1'
elif '1' in cardinality_text:
    cardinality = '1'
elif '1..*' in cardinality_text:
    cardinality = '1..*'


# Print the detected cardinality
print('Cardinality:', cardinality)
