import cv2
import pytesseract

# Load the image
img = cv2.imread('class0.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to binarize the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Apply OCR to recognize text in the image
text = pytesseract.image_to_string(thresh, lang="eng", config='--psm 11')

# Split the text into lines
lines = text.split('\n')

# Iterate over each line
for line in lines:
    # Check if the line matches the pattern for a UML class shape
    if "class" in line and "{" in line and "}" in line:
        # Process the class shape
        class_name = line.split("class")[1].split("{")[0].strip()
        attributes = line.split("{")[1].split("}")[0].strip()
        methods = line.split("}")[1].strip()
        print("Class name: {}".format(class_name))
        print("Attributes: {}".format(attributes))
        print("Methods: {}".format(methods))
    elif "interface" in line and "{" in line and "}" in line:
        # Process the interface shape
        interface_name = line.split("interface")[1].split("{")[0].strip()
        methods = line.split("{")[1].split("}")[0].strip()
        print("Interface name: {}".format(interface_name))
        print("Methods: {}".format(methods))
