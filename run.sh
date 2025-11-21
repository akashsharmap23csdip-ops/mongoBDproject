#!/bin/bash

# Complete Run Script - Executes all project phases in sequence

echo "============================================================"
echo "MongoDB Amazon Food Reviews Analysis"
echo "Complete Project Execution"
echo "============================================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Phase 1: Data Ingestion
echo ""
echo "PHASE 1: Data Ingestion & Sentiment Analysis"
echo "------------------------------------------------------------"
read -p "Load data into MongoDB? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python ingest_data.py
    if [ $? -ne 0 ]; then
        echo "❌ Data ingestion failed!"
        exit 1
    fi
else
    echo "Skipping data ingestion..."
fi

# Phase 2: Test Pipelines
echo ""
echo "PHASE 2: Testing Aggregation Pipelines"
echo "------------------------------------------------------------"
read -p "Test aggregation pipelines? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python aggregation_pipelines.py
    if [ $? -ne 0 ]; then
        echo "❌ Pipeline testing failed!"
        exit 1
    fi
else
    echo "Skipping pipeline testing..."
fi

# Phase 3: Start Flask Server
echo ""
echo "PHASE 3: Starting Flask API Server"
echo "------------------------------------------------------------"
echo "Starting server at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
