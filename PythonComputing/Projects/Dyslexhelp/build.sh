#!/bin/bash

# Create and activate virtual environment (if it doesn't exist)
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
brew install tesseract  # Or appropriate Tesseract installation for your OS

# Set environment variable AND run the app in the SAME shell session
export GOOGLE_APPLICATION_CREDENTIALS="/Users/dhanvins_com/PythonComputing/Projects/dotted-task-451114-s6-dc663783f317.json" python3 main.py

deactivate # Deactivate virtual environment (after the app finishes)