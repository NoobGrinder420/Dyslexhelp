#!/bin/bash

# Create and activate virtual environment (if it doesn't exist)
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variable AND run the app in the SAME shell session
export GOOGLE_APPLICATION_CREDENTIALS="" #Change to your google cloud API json file

python3 ../app/main.py

deactivate # Deactivate virtual environment (after the app finishes)
