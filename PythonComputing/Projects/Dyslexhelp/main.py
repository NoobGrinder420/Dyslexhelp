from flask import Flask, render_template, request, redirect, url_for
import random
import cv2
import numpy as np
import os
import traceback
import uuid
from google.cloud import vision

app = Flask(__name__, template_folder='templates', static_folder='static')

# Sample phrases
phrases = [
    "The quick brown fox jumps over the lazy dog.",
    "Hello World!",
    "Practice makes perfect.",
    "Python is fun!"
]
generated_phrase = ""

# Ensure template directory exists
os.makedirs('templates', exist_ok=True)

# HTML template files (create if they don't exist)
templates = {
    'home.html': """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dyslexhelp</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <a href='/generate'>Start</a>
    </body>
    </html>
    """,
    'generate.html': """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Phrase</title>
    </head>
    <body>
        <h1>Generated Phrase</h1>
        <p>{{ phrase }}</p>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <button type="submit">Upload Image</button>
        </form>
    </body>
    </html>
    """,
    'result.html': """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Result</title>
    </head>
    <body>
        <h1>Generated Phrase: {{ phrase }}</h1>
        <h2>Extracted Text: {{ extracted }}</h2>

        {% if errors %}
        <h3>Errors:</h3>
        <ul>
            {% for i, char in errors %}
                <li>Error at index {{ i }}: Expected '{{ char }}', Got '{{ extracted[i] if i < extracted|length else ' ' }}'</li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No errors found!</p>
        {% endif %}

        <a href="/generate">Try Again</a>
    </body>
    </html>
    """
}

for filename, content in templates.items():
    if not os.path.exists(f'templates/{filename}'):
        with open(f'templates/{filename}', 'w') as f:
            f.write(content)

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
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Generate a unique filename for the images
        unique_id = uuid.uuid4()
        image_base_name = f"processed_image_{unique_id}"

        # 1. Save the original uploaded image for debugging
        original_image_path = f"static/{image_base_name}_uploaded.jpg"
        cv2.imwrite(original_image_path, img)

        # Image Preprocessing (more robust)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_image_path = f"static/{image_base_name}_gray.jpg"
        cv2.imwrite(gray_image_path, gray)

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        blurred_image_path = f"static/{image_base_name}_blurred.jpg"
        cv2.imwrite(blurred_image_path, blurred)

        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)
        thresh_image_path = f"static/{image_base_name}_thresh.jpg"
        cv2.imwrite(thresh_image_path, thresh)

        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        opened_image_path = f"static/{image_base_name}_opened.jpg"
        cv2.imwrite(opened_image_path, opening)


        # Initialize the Vision API client
        client = vision.ImageAnnotatorClient()

        # Convert the preprocessed image to bytes (required for the API)
        _, encoded_image = cv2.imencode('.png', opening)  # Encode the 'opening' image
        content = encoded_image.tobytes()

        image = vision.Image(content=content)

        # Perform OCR using the Vision API
        response = client.text_detection(image=image)
        texts = response.text_annotations

        extracted_text = ""
        if texts:
            # The first text annotation is the entire detected text
            extracted_text = texts[0].description

        # Error Checking (improved)
        errors = []
        for i, char in enumerate(generated_phrase):
            if i >= len(extracted_text) or char != extracted_text[i]:
                expected = char
                errors.append((i, expected))

        return render_template('result.html', phrase=generated_phrase, extracted=extracted_text, errors=errors)

    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred: {e}"
        return render_template('result.html', phrase=generated_phrase, extracted=error_message, errors=[(0, "Error")])

if __name__ == '__main__':
    app.run(debug=True)