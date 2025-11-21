#!/bin/bash

# Quick Setup Script for MongoDB Amazon Food Reviews Analysis Project

echo "============================================================"
echo "MongoDB Amazon Food Reviews Analysis - Quick Setup"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if MongoDB is running
if ! command -v mongosh &> /dev/null && ! command -v mongo &> /dev/null; then
    echo "⚠️  MongoDB CLI not found. Assuming MongoDB is running..."
else
    echo "✓ MongoDB CLI found"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download TextBlob corpora
echo "Downloading TextBlob corpora..."
python -m textblob.download_corpora > /dev/null 2>&1

# Extract dataset if needed
if [ ! -f "amazon Food Reviews 100k Dataset.csv" ]; then
    if [ -f "amazon Food Reviews 100k Dataset.csv.zip" ]; then
        echo "Extracting dataset..."
        unzip -q "amazon Food Reviews 100k Dataset.csv.zip"
        echo "✓ Dataset extracted"
    else
        echo "⚠️  Dataset ZIP file not found!"
    fi
else
    echo "✓ Dataset already extracted"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
fi

echo ""
echo "============================================================"
echo "✓ Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Ensure MongoDB is running on localhost:27017"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Load data: python ingest_data.py"
echo "4. Start server: python app.py"
echo "5. Open browser: http://localhost:5000"
echo ""
echo "============================================================"
