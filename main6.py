import cv2
import pytesseract

# Load the image and convert it to grayscale
image = cv2.imread('class.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection to find contours
edges = cv2.Canny(gray, 100, 200)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Find the contour with the largest area
largest_contour = max(contours, key=cv2.contourArea)

# Get the bounding box of the contour
x, y, w, h = cv2.boundingRect(largest_contour)

# Crop the image to the bounding box
crop = image[y:y+h, x:x+w]

# Extract text using Pytesseract
text = pytesseract.image_to_string(crop)

# Print the extracted text
print(text)
