#!/bin/bash

# Determine the operating system
OS_TYPE=$(uname -s)

# Set variables based on the operating system
if [ "$OS_TYPE" = "Darwin" ]; then
    CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/mac-arm64/chromedriver-mac-arm64.zip"
    CHROMEDRIVER_ZIP="chromedriver-mac-arm64.zip"
    CHROMEDRIVER_EXTRACTED_DIR="chromedriver-mac-arm64"
elif [ "$OS_TYPE" = "Linux" ]; then
    CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip"
    CHROMEDRIVER_ZIP="chromedriver-linux64.zip"
    CHROMEDRIVER_EXTRACTED_DIR="chromedriver-linux64"
else
    echo "Unsupported OS: $OS_TYPE"
    exit 1
fi

CHROMEDRIVER_DIR="chromedriver"

# Download ChromeDriver
echo "Downloading ChromeDriver..."
curl -o $CHROMEDRIVER_ZIP $CHROMEDRIVER_URL

# Unzip ChromeDriver
echo "Unzipping ChromeDriver..."
unzip $CHROMEDRIVER_ZIP

# Rename the extracted directory to a consistent name
mv $CHROMEDRIVER_EXTRACTED_DIR $CHROMEDRIVER_DIR

# Remove the zip file
rm $CHROMEDRIVER_ZIP

# Create and activate a virtual environment
echo "Creating virtual environment..."
python3 -m venv env

# Install required packages
echo "Installing required packages..."
source env/bin/activate
pip install -r requirements.txt

# Notify user of completion
echo "Setup complete. To activate the virtual environment, run:"
echo "source env/bin/activate"
echo "Then you can run the script with:"
echo "python intercept.py <URL>"
