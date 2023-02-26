import pytesseract
import cv2

# Load the class diagram image
img = cv2.imread('class.png')

# Define the area containing the cardinality text
x, y, w, h = 100, 200, 200, 50
roi = img[y:y+h, x:x+w]

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
