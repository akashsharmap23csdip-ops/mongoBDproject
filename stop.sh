#!/bin/bash

# Stop Script for MongoDB Amazon Food Reviews Analysis
# This script stops the Flask application and optionally MongoDB

echo "============================================================"
echo "Stopping MongoDB Amazon Food Reviews Analysis"
echo "============================================================"

# Stop Flask application
echo ""
echo "Step 1: Stopping Flask server..."
if [ -f ".flask.pid" ]; then
    FLASK_PID=$(cat .flask.pid)
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        kill $FLASK_PID 2>/dev/null
        sleep 1
        if ps -p $FLASK_PID > /dev/null 2>&1; then
            kill -9 $FLASK_PID 2>/dev/null
        fi
        echo "✓ Flask server stopped (PID: $FLASK_PID)"
    else
        echo "✓ Flask server was not running"
    fi
    rm .flask.pid
else
    # Try to kill any Python process on port 5000
    if lsof -ti:5000 > /dev/null 2>&1; then
        lsof -ti:5000 | xargs kill -9 2>/dev/null
        echo "✓ Stopped process on port 5000"
    else
        echo "✓ No Flask server running on port 5000"
    fi
fi

# Ask if user wants to stop MongoDB
echo ""
echo "Step 2: MongoDB service..."
read -p "Do you want to stop MongoDB? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v systemctl &> /dev/null; then
        # Linux with systemd
        if systemctl is-active --quiet mongodb; then
            sudo systemctl stop mongodb
            echo "✓ MongoDB stopped"
        else
            echo "✓ MongoDB was not running"
        fi
    elif command -v brew &> /dev/null; then
        # macOS with Homebrew
        if brew services list | grep mongodb-community | grep started &> /dev/null; then
            brew services stop mongodb-community
            echo "✓ MongoDB stopped"
        else
            echo "✓ MongoDB was not running"
        fi
    else
        echo "⚠️  Please stop MongoDB manually if needed"
    fi
else
    echo "✓ MongoDB left running"
fi

echo ""
echo "============================================================"
echo "✓ Application stopped successfully!"
echo "============================================================"
echo ""
echo "To start again: ./start.sh"
echo ""
