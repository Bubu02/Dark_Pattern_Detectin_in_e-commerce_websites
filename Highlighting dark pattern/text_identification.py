import time
import pytesseract
import pyautogui
import json
from PIL import Image
from joblib import load
from sklearn.feature_extraction.text import CountVectorizer

# Load the file paths from the JSON file
with open(r"C:\Users\mebub_9a7jdi8\Desktop\Dark pattern detection in e-commerce website\Path\paths.json") as f:
    file_paths = json.load(f)

# Set the tesseract path from the JSON file
pytesseract.pytesseract.tesseract_cmd = file_paths["TESSERACT_PATH"]

# Load the trained model
model = load(file_paths["MODEL_JOBLIB"])

# Load the trained vectorizer
vectorizer = load(file_paths["VECTORIZER"])

def extract_text_from_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Use pytesseract to convert the screenshot into text
    text = pytesseract.image_to_string(screenshot)
    return text

while True:
    # Extract text from screen
    text = extract_text_from_screen()
    # Convert the text to a numerical matrix
    X = vectorizer.transform([text])
    # Use the model to predict if the text is a dark pattern
    prediction = model.predict(X)
    # If the text is a dark pattern, print it
    if prediction[0] == 1:  # assuming 1 means dark pattern
        print(text)
    # Wait for a bit before taking the next screenshot
    time.sleep(5)
