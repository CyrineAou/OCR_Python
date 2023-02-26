
import cv2
import pytesseract

# Load the image and convert it to grayscale
image = cv2.imread('class1.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply image pre-processing
threshold = 150
gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

# Extract text using Pytesseract
text = pytesseract.image_to_string(gray)

# Print the extracted text
print(text)
