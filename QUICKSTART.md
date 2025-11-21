# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ MongoDB running on `localhost:27017`
- ✅ 2GB free disk space

### Step 1: Setup (2 minutes)

```bash
# Clone or navigate to project directory
cd /workspaces/mongoBDproject

# Run automatic setup
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

**Windows users:**
```cmd
setup.bat
venv\Scripts\activate
```

### Step 2: Load Data (2 minutes)

```bash
python ingest_data.py
```

Wait for confirmation message:
```
✓ Successfully inserted 100000 documents!
```

### Step 3: Start Server (1 minute)

```bash
python app.py
```

### Step 4: View Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

You should see three interactive charts analyzing the Amazon food reviews! 🎉

---

## Troubleshooting

### MongoDB Not Running?

**Linux/Ubuntu:**
```bash
sudo systemctl start mongodb
sudo systemctl status mongodb
```

**macOS:**
```bash
brew services start mongodb-community
```

**Windows:**
- Start MongoDB from Services or MongoDB Compass

### Port 5000 Already in Use?

Edit `.env` file:
```
FLASK_PORT=8080
```

Then restart the server.

### Import Errors?

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

## What's Next?

### Explore the API

Try these endpoints in your browser:

- **Health Check**: http://localhost:5000/api/health
- **Sentiment Analysis**: http://localhost:5000/api/sentiment_by_rating
- **Length Analysis**: http://localhost:5000/api/content_length_vs_rating
- **Distribution**: http://localhost:5000/api/rating_distribution_by_sentiment

### View Database

Using MongoDB shell:
```bash
mongosh
use amazon_food_reviews
db.reviews.countDocuments()
db.reviews.findOne()
```

### Test Pipelines

Run pipelines independently:
```bash
python aggregation_pipelines.py
```

### Get Database Stats

```bash
python db_utils.py
```

---

## Project Structure

```
mongoBDproject/
├── ingest_data.py              # Load data into MongoDB
├── aggregation_pipelines.py   # Three complex pipelines
├── app.py                      # Flask API server
├── templates/
│   └── dashboard.html          # Web dashboard
├── README.md                   # Full documentation
└── PIPELINE_DOCS.md           # Pipeline explanations
```

---

## Common Commands

```bash
# Setup
./setup.sh                    # Initial setup

# Data Operations
python ingest_data.py        # Load data
python db_utils.py          # View stats

# Server
python app.py               # Start API server
./run.sh                    # Run complete workflow

# Testing
python aggregation_pipelines.py  # Test pipelines
curl http://localhost:5000/api/health  # Test API
```

---

## Need Help?

- 📖 Full Documentation: `README.md`
- 🔍 Pipeline Details: `PIPELINE_DOCS.md`
- 🐛 Check the troubleshooting section in README

---

**Happy Analyzing! 🍎📊**
