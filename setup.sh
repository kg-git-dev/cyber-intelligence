#!/bin/bash

# Update package manager and install necessary packages
sudo apt-get update
sudo apt-get install -y python3-pip chromium-driver

# Create virtual environment
echo "Creating virtual environment..."
virtualenv env

# Activate virtual environment and install dependencies
source env/bin/activate
pip install -r requirements.txt

echo "Setup complete. To activate the virtual environment, run:"
echo "source env/bin/activate"
echo "run script with python intercept.py http://google.com"
