# Dyslexhelp
The main branch uses Google Cloud Vision API, which requires billing information.\
If you do not wish to provide billing information for the API key, visit other branches.

Co-created with See Kaishen Bryan & Luis Santino Maramag Ugay.

---

### Setup Instructions

1. **Change Directory**: Navigate to the project directory:
   ```bash
   cd dyslexhelp
   ```

2. **Run the Build Script**: Use the following command to run the setup:
   ```bash
   ./build/build.sh
   ```

### Features

- **Random Phrase Generation**: A predefined list of phrases is randomly selected for each user session.
- **Image Upload**: Users can upload an image containing text.
- **Image Preprocessing**: The uploaded image is processed to improve text extraction quality using OpenCV.
- **OCR (Optical Character Recognition)**: The app utilizes Google Cloud Vision API to extract text from the uploaded image.
- **Text Comparison**: The extracted text is compared with the generated phrase, and any discrepancies are highlighted.
- **Error Highlighting**: The app displays the exact positions where the extracted text differs from the expected phrase.
- **Error Handling**: The app includes robust error handling to ensure smooth operation, even when something goes wrong during the image processing or OCR steps.

### Requirements

Before running the application, ensure that you have the following:

- Python 3.7 or higher
- Flask (Web framework)
- OpenCV (for image processing)
- NumPy (for numerical operations)
- Google Cloud Vision Client Library (for OCR)
- Google Cloud account and Vision API enabled
- A text editor or Integrated Development Environment (IDE)

### Running the App

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/NoobGrinder420/Dyslexhelp.git
   cd Dyslexhelp
   ```

2. **Install Dependencies**

   Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud Vision API Credentials**

   Make sure your Google Cloud Vision API credentials are properly set up. You can follow the official [Google Cloud Vision Setup Guide](https://cloud.google.com/vision/docs/setup) for this.

4. **Run the Application**

   After everything is set up, you can run the Flask app with the following command:

   ```bash
   python app.py
   ```

   The app should now be running locally at `http://127.0.0.1:5000/`.

5. **Accessing the App**

   Open your web browser and go to `http://127.0.0.1:5000/`. You will see the homepage with an option to generate a random phrase.

6. **Uploading an Image**

   On the `/generate` page, you will see a random phrase. You can upload an image that contains text, and the app will perform OCR to extract the text from the image and compare it with the generated phrase.

### How It Works

1. **Home Route (`/`)**

   When users visit the homepage, the `home.html` template is rendered. This page serves as the starting point for the application.

2. **Generate Route (`/generate`)**

   On visiting the `/generate` route, the app selects a random phrase from a predefined list and displays it on the page. This is the phrase that the user will attempt to match with the text extracted from their uploaded image.

3. **Upload Route (`/upload`)**

   This route handles the image upload. When a user submits a file, the image is read using OpenCV and processed for OCR. The app performs several preprocessing steps to improve the accuracy of the text extraction.

4. **Text Comparison**

   The app compares the extracted text with the generated phrase and identifies where the discrepancies occur. If any mismatch is found, it is highlighted in the final result.

5. **Result Page (`/result`)**

   After OCR and text comparison, the user is shown the results on the `result.html` page. The page displays the original phrase, the extracted text, and any errors or discrepancies.

### Conclusion

Dyslexhelp demonstrates how web technologies like Flask, image processing with OpenCV, and OCR via Google Cloud Vision can assist dyslexic individuals. It provides a way to visually compare OCR results with a predefined text, helping users identify discrepancies. This app can be expanded with features like multiple language support, a larger set of phrases, or the ability to upload multiple images for processing.
