#!/bin/bash

# Update package manager and install necessary packages
sudo apt-get update
sudo apt-get install -y python3-pip virtualenv chromium-driver chromium-browser \
    libx11-xcb1 libnss3 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libxss1 libasound2 libatk1.0-0 libgtk-3-0

# Create virtual environment
echo "Creating virtual environment..."
virtualenv env

# Activate virtual environment and install dependencies
source env/bin/activate
pip install -r requirements.txt

echo "Setup complete. To activate the virtual environment, run:"
echo "source env/bin/activate"
echo "Then you can run your script."
