#!/bin/bash

# Start Script for MongoDB Amazon Food Reviews Analysis
# This script starts MongoDB and the Flask application

echo "============================================================"
echo "Starting MongoDB Amazon Food Reviews Analysis"
echo "============================================================"

# Check if MongoDB is installed
if ! command -v mongod &> /dev/null && ! command -v systemctl &> /dev/null; then
    echo "⚠️  MongoDB not found. Please install MongoDB first."
    exit 1
fi

# Start MongoDB if not running
echo ""
echo "Step 1: Starting MongoDB..."
if command -v systemctl &> /dev/null; then
    # Linux with systemd
    if systemctl is-active --quiet mongodb; then
        echo "✓ MongoDB is already running"
    else
        echo "Starting MongoDB service..."
        sudo systemctl start mongodb
        sleep 2
        if systemctl is-active --quiet mongodb; then
            echo "✓ MongoDB started successfully"
        else
            echo "❌ Failed to start MongoDB. Please start it manually."
            exit 1
        fi
    fi
elif command -v brew &> /dev/null; then
    # macOS with Homebrew
    if brew services list | grep mongodb-community | grep started &> /dev/null; then
        echo "✓ MongoDB is already running"
    else
        echo "Starting MongoDB service..."
        brew services start mongodb-community
        sleep 2
        echo "✓ MongoDB started"
    fi
else
    echo "⚠️  Please ensure MongoDB is running manually"
fi

# Check if virtual environment exists
echo ""
echo "Step 2: Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Check if data is loaded
echo ""
echo "Step 3: Checking database..."
python -c "
from pymongo import MongoClient
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    db = client['amazon_food_reviews']
    count = db['reviews'].count_documents({})
    if count > 0:
        print(f'✓ Database ready with {count:,} reviews')
    else:
        print('⚠️  Database is empty. Run: python ingest_data.py')
    client.close()
except Exception as e:
    print(f'⚠️  Could not connect to database: {e}')
" 2>/dev/null || echo "⚠️  Could not check database"

# Start Flask application in background
echo ""
echo "Step 4: Starting Flask server..."
echo "------------------------------------------------------------"

# Kill any existing Flask process on port 5000
lsof -ti:5000 | xargs kill -9 2>/dev/null

# Start Flask in background and save PID
nohup python app.py > flask.log 2>&1 &
FLASK_PID=$!
echo $FLASK_PID > .flask.pid

# Wait a moment for server to start
sleep 3

# Check if server is running
if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "✓ Flask server started successfully (PID: $FLASK_PID)"
    echo ""
    echo "============================================================"
    echo "✓ Application is running!"
    echo "============================================================"
    echo ""
    echo "Dashboard:  http://localhost:5000"
    echo "API Health: http://localhost:5000/api/health"
    echo ""
    echo "Server logs: tail -f flask.log"
    echo "Stop server: ./stop.sh"
    echo ""
    echo "============================================================"
else
    echo "❌ Failed to start Flask server"
    echo "Check flask.log for errors"
    exit 1
fi
