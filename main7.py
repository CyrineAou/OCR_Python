import cv2
import pytesseract

# Load the image and convert it to grayscale

image = cv2.imread('class3.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply image pre-processing
threshold = 150

gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

# Find contours in the image
contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop over the contours and extract text from each
for contour in contours:
    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Crop the image to the bounding box
    crop = gray[y:y+h, x:x+w]

    # Extract text using Pytesseract
    text = pytesseract.image_to_string(crop)

    # Print the extracted text
    print(text)
