import cv2
import pytesseract
import json
import requests

def detect_text(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image to improve OCR accuracy
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to convert it into a binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply noise removal techniques to remove noise from the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Set the path to the Tesseract OCR executable file
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Pass the preprocessed image to the Tesseract OCR engine
    text = pytesseract.image_to_string(opening)

    # Calculate the degree of precision
    degree_of_precision = len(text) / (image.shape[0] * image.shape[1])

    # Create a dictionary to store the output
    output = {'text': text.strip(), 'degree_of_precision': degree_of_precision}

    # Convert the dictionary to JSON format
    json_output = json.dumps(output)

    # Send the JSON output to the Node.js server
    headers = {'Content-type': 'application/json'}
    response = requests.post('http://localhost:3000/api/ocr', data=json_output, headers=headers)

    return response.text

# Call the detect_text function with the path to the class diagram image
response = detect_text('class.png')

# Print the response from the server
print(response)
