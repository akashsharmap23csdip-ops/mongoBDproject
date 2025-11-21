@echo off
REM Quick Setup Script for MongoDB Amazon Food Reviews Analysis Project (Windows)

echo ============================================================
echo MongoDB Amazon Food Reviews Analysis - Quick Setup
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo + Python found
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Download TextBlob corpora
echo Downloading TextBlob corpora...
python -m textblob.download_corpora >nul 2>&1

REM Extract dataset if needed
if not exist "amazon Food Reviews 100k Dataset.csv" (
    if exist "amazon Food Reviews 100k Dataset.csv.zip" (
        echo Extracting dataset...
        tar -xf "amazon Food Reviews 100k Dataset.csv.zip"
        echo + Dataset extracted
    ) else (
        echo ! Dataset ZIP file not found!
    )
) else (
    echo + Dataset already extracted
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo + .env file created
)

echo.
echo ============================================================
echo + Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Ensure MongoDB is running on localhost:27017
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Load data: python ingest_data.py
echo 4. Start server: python app.py
echo 5. Open browser: http://localhost:5000
echo.
echo ============================================================

pause
