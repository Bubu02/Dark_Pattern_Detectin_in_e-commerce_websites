import time
import pytesseract
import pyautogui
import json
from PIL import Image
from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os

# Load the file paths from the JSON file
with open("./Path/paths.json") as f:
    file_paths = json.load(f)

# Set the tesseract path from the JSON file
pytesseract.pytesseract.tesseract_cmd = file_paths["TESSERACT_PATH"]

# Load the trained model
model = load(file_paths["MODEL_JOBLIB"])

# Load the trained vectorizer
vectorizer = load(file_paths["VECTORIZER"])

# Create a DataFrame to store the dark patterns and their labels
df = pd.DataFrame(columns=["Dark Pattern", "Label"])

# Path to the Excel file
excel_file = file_paths["DETECTED_DATA"]

def extract_text_from_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Use pytesseract to convert the screenshot into text
    text = pytesseract.image_to_string(screenshot)
    return text

def ask_user(line):
    # Create a new Tkinter window
    window = tk.Tk()
    window.withdraw()  # Hide the main window

    # Show a messagebox and get the user's response
    response = messagebox.askyesno("Dark Pattern Detected", "Do you want to print it?")
     # Bring the window to the foreground and keep it on top
    window.lift()
    window.attributes('-topmost', True)
    window.destroy()

    return response

while True:
    # Extract text from screen
    text = extract_text_from_screen()
    # Split the text into lines
    lines = text.split('\n')
    for line in lines:
        # Convert the line to a numerical matrix
        X = vectorizer.transform([line])
        # Use the model to predict if the line is a dark pattern
        prediction = model.predict(X)
        # If the line is a dark pattern, ask the user if they want to print it
        if prediction[0] == 1:
            if ask_user(line):
                print(line)
                df = df._append({"Dark Pattern": line, "Label": 1}, ignore_index=True)
            else:
                # If the Excel file exists, read it into a DataFrame
                if os.path.exists(excel_file):
                    df_old = pd.read_excel(excel_file)
                    df = pd.concat([df_old, df])
                # Save the DataFrame to an Excel file
                df.to_excel(excel_file, index=False)
                exit(0)  # Exit the program
    # Wait for a bit before taking the next screenshot
    time.sleep(5)
