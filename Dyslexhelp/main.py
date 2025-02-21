from flask import Flask, render_template, request, redirect, url_for, send_file
import random
import cv2
import numpy as np
import os
import traceback
import uuid
from spellchecker import SpellChecker
from autocorrect import Speller
from PIL import Image
import pytesseract

app = Flask(__name__, template_folder='templates', static_folder='static')

# Define the upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Sample phrases
phrases = [
    "The quick brown fox jumps over the lazy dog.",
    "Hello World!",
    "Practice makes perfect.",
    "Python is fun!"
]
generated_phrase = ""

def readerMain(filename):
    spell = SpellChecker()
    spell2 = Speller(lang="en")

    # Load and process the image
    img = np.array(Image.open(filename).convert("L"))  # Convert to grayscale
    norm_img = np.zeros((img.shape[0], img.shape[1]))

    # Normalize and preprocess the image
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (1, 1), 0)

    def convert(lst):
        return [i for item in lst for i in item.split()]

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(img)
    ctext = convert([extracted_text])
    scheckedtext = []

    # Process each word and correct spelling
    for i in ctext:
        corrected_word = spell.correction(i)
        if corrected_word:  # Only process if the word is not None
            i = spell2(corrected_word)
        scheckedtext.append(i)

    # Add spacing for formatting
    scheckedtext = ["  "] * 7 + scheckedtext  

    return " ".join(scheckedtext)  # Return the processed text

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate')
def generate():
    global generated_phrase
    generated_phrase = random.choice(phrases)
    return render_template('generate.html', phrase=generated_phrase)

@app.route('/upload', methods=['POST'])
def upload():
    global generated_phrase
    file = request.files.get('file')
    if not file or file.filename == '':
        return redirect(url_for('generate'))

    try:
        # Generate a unique filename for the uploaded image
        unique_id = uuid.uuid4()
        image_filename = f"{unique_id}.jpg"
        image_filepath = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
        file.save(image_filepath)

        # Process the uploaded image
        extracted_text = readerMain(image_filepath)

        # Save extracted text to a file
        text_filename = f"{unique_id}.txt"
        text_filepath = os.path.join(app.config["UPLOAD_FOLDER"], text_filename)
        with open(text_filepath, "w") as text_file:
            text_file.write(extracted_text)

        # Compare extracted text with the generated phrase
        errors = []
        for i, char in enumerate(generated_phrase):
            if i >= len(extracted_text) or char != extracted_text[i]:
                errors.append((i, char))  # Expected character

        return render_template('result.html', phrase=generated_phrase, extracted=extracted_text, errors=errors, text_file=text_filename)

    except Exception as e:
        traceback.print_exc()
        return render_template('result.html', phrase=generated_phrase, extracted=f"Error: {e}", errors=[(0, "Error")])

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
