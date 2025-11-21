# Command Reference Guide

Complete list of all commands for the MongoDB Amazon Food Reviews Analysis project.

---

## 📦 Installation & Setup

### Initial Setup (Automated)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Manual Setup

**Create Virtual Environment:**
```bash
python3 -m venv venv
```

**Activate Virtual Environment:**
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Download TextBlob Data:**
```bash
python -m textblob.download_corpora
```

**Extract Dataset:**
```bash
unzip "amazon Food Reviews 100k Dataset.csv.zip"
```

---

## 🗄️ MongoDB Commands

### Start/Stop MongoDB

**Linux (Ubuntu/Debian):**
```bash
# Start
sudo systemctl start mongodb

# Stop
sudo systemctl stop mongodb

# Status
sudo systemctl status mongodb

# Enable on boot
sudo systemctl enable mongodb
```

**macOS:**
```bash
# Start
brew services start mongodb-community

# Stop
brew services stop mongodb-community

# Status
brew services list
```

**Windows:**
```cmd
# Start (as Administrator)
net start MongoDB

# Stop
net stop MongoDB
```

### MongoDB Shell

**Connect to Database:**
```bash
# Modern shell
mongosh

# Legacy shell
mongo
```

**Database Operations:**
```javascript
// Use database
use amazon_food_reviews

// Count documents
db.reviews.countDocuments()

// View sample document
db.reviews.findOne()

// View all collections
show collections

// Get collection stats
db.reviews.stats()

// View indexes
db.reviews.getIndexes()

// Count by rating
db.reviews.countDocuments({Rating: 5})

// Find negative sentiment
db.reviews.find({sentiment_score: {$lt: 0}}).limit(5)

// Average sentiment
db.reviews.aggregate([
  {$group: {_id: null, avg: {$avg: "$sentiment_score"}}}
])
```

---

## 🐍 Python Scripts

### Data Ingestion

**Run Data Ingestion:**
```bash
python ingest_data.py
```

**With Custom MongoDB URI:**
```bash
MONGO_URI="mongodb://localhost:27017/" python ingest_data.py
```

### Test Aggregation Pipelines

**Run Pipeline Tests:**
```bash
python aggregation_pipelines.py
```

### Start Flask Server

**Development Mode:**
```bash
python app.py
```

**Production Mode:**
```bash
FLASK_DEBUG=False python app.py
```

**Custom Port:**
```bash
FLASK_PORT=8080 python app.py
```

**Custom Host:**
```bash
FLASK_HOST=127.0.0.1 python app.py
```

### Database Utilities

**Get Database Stats:**
```bash
python db_utils.py
```

**Clear Collection (in Python):**
```python
from db_utils import clear_collection
clear_collection()
```

**Drop Database (in Python):**
```python
from db_utils import drop_database
drop_database()
```

---

## 🌐 API Testing Commands

### Using curl

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Sentiment by Rating:**
```bash
curl http://localhost:5000/api/sentiment_by_rating
```

**Content Length vs Rating:**
```bash
curl http://localhost:5000/api/content_length_vs_rating
```

**Rating Distribution:**
```bash
curl http://localhost:5000/api/rating_distribution_by_sentiment
```

**All Analytics:**
```bash
curl http://localhost:5000/api/all_analytics
```

**Formatted JSON Output:**
```bash
curl http://localhost:5000/api/health | python -m json.tool
```

**Save Response to File:**
```bash
curl http://localhost:5000/api/all_analytics > analytics.json
```

### Using httpie (if installed)

```bash
# Install httpie
pip install httpie

# Make requests
http GET http://localhost:5000/api/health
http GET http://localhost:5000/api/sentiment_by_rating
```

### Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# All analytics
response = requests.get('http://localhost:5000/api/all_analytics')
data = response.json()
print(f"Total reviews: {data['total_reviews']}")
```

---

## 🚀 Run Scripts

### Complete Workflow

**Interactive Run:**
```bash
chmod +x run.sh
./run.sh
```

**Non-Interactive (Auto-yes):**
```bash
yes | ./run.sh
```

---

## 🧪 Testing & Debugging

### Check Python Version

```bash
python --version
python3 --version
```

### Verify Dependencies

```bash
pip list
pip freeze
```

### Check Specific Package

```bash
pip show pymongo
pip show flask
pip show textblob
```

### Test MongoDB Connection

```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
print(client.server_info())
```

### Test TextBlob

```python
from textblob import TextBlob
blob = TextBlob("This is a great product!")
print(blob.sentiment)
```

### View Flask Routes

```python
# Add to app.py temporarily
@app.before_first_request
def show_routes():
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
```

### Enable Flask Debug Mode

```bash
FLASK_DEBUG=True python app.py
```

### Check Port Usage

**Linux/macOS:**
```bash
lsof -i :5000
```

**Windows:**
```cmd
netstat -ano | findstr :5000
```

### Kill Process on Port

**Linux/macOS:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Windows:**
```cmd
# Find PID first, then:
taskkill /PID <pid> /F
```

---

## 📊 Data Analysis Commands

### Pandas in Python

```python
import pandas as pd

# Read CSV
df = pd.read_csv('amazon Food Reviews 100k Dataset.csv')

# Basic stats
print(df.describe())
print(df.info())
print(df.head())

# Rating distribution
print(df['Rating'].value_counts().sort_index())

# Average review length
df['length'] = df['Review'].str.len()
print(df.groupby('Rating')['length'].mean())
```

### MongoDB Aggregation Examples

```javascript
// Count reviews per rating
db.reviews.aggregate([
  {$group: {_id: "$Rating", count: {$sum: 1}}},
  {$sort: {_id: 1}}
])

// Average content length by rating
db.reviews.aggregate([
  {$group: {
    _id: "$Rating",
    avg_length: {$avg: "$content_length"}
  }},
  {$sort: {_id: 1}}
])

// Top 10 most positive reviews
db.reviews.find().sort({sentiment_score: -1}).limit(10)

// Top 10 most negative reviews
db.reviews.find().sort({sentiment_score: 1}).limit(10)

// Reviews with mismatch (5 stars but negative sentiment)
db.reviews.find({
  Rating: 5,
  sentiment_score: {$lt: 0}
}).limit(10)
```

---

## 🔧 Maintenance Commands

### Update Dependencies

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### Freeze Current Dependencies

```bash
pip freeze > requirements.txt
```

### Clean Python Cache

```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Backup MongoDB Database

```bash
mongodump --db amazon_food_reviews --out backup/
```

### Restore MongoDB Database

```bash
mongorestore --db amazon_food_reviews backup/amazon_food_reviews/
```

### Export Collection to JSON

```bash
mongoexport --db amazon_food_reviews --collection reviews --out reviews.json
```

### Import Collection from JSON

```bash
mongoimport --db amazon_food_reviews --collection reviews --file reviews.json
```

---

## 🐳 Docker Commands (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build Docker Image

```bash
docker build -t amazon-reviews-analysis .
```

### Run Docker Container

```bash
docker run -p 5000:5000 -e MONGO_URI=mongodb://host.docker.internal:27017/ amazon-reviews-analysis
```

### Docker Compose

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
  
  app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    environment:
      - MONGO_URI=mongodb://mongodb:27017/

volumes:
  mongodb_data:
```

**Run with Docker Compose:**
```bash
docker-compose up -d
```

---

## 📝 Git Commands

### Initial Commit

```bash
git init
git add .
git commit -m "Initial commit: MongoDB Amazon Food Reviews Analysis"
```

### Push to GitHub

```bash
git remote add origin https://github.com/yourusername/mongoBDproject.git
git branch -M main
git push -u origin main
```

### Update .gitignore

```bash
echo "venv/" >> .gitignore
echo "*.csv" >> .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

---

## 🌐 Browser Commands

### Open Dashboard

**Linux:**
```bash
xdg-open http://localhost:5000
```

**macOS:**
```bash
open http://localhost:5000
```

**Windows:**
```cmd
start http://localhost:5000
```

**Cross-platform (Python):**
```bash
python -m webbrowser http://localhost:5000
```

---

## 📈 Performance Monitoring

### Python Memory Usage

```python
import tracemalloc

tracemalloc.start()
# Your code here
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

### MongoDB Performance

```javascript
// Enable profiling
db.setProfilingLevel(2)

// View slow queries
db.system.profile.find().sort({ts: -1}).limit(5)

// Explain query
db.reviews.find({Rating: 5}).explain("executionStats")
```

### Flask Request Timing

```python
from flask import g
import time

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(f"Request took: {diff:.3f} seconds")
    return response
```

---

## 🛠️ Troubleshooting Commands

### Check Python Path

```bash
which python
which python3
```

### Check MongoDB Status

```bash
ps aux | grep mongo
```

### Check Network Connections

```bash
netstat -an | grep 5000
netstat -an | grep 27017
```

### View Process List

```bash
ps aux | grep python
ps aux | grep mongo
```

### Check Disk Space

```bash
df -h
```

### Check Memory Usage

```bash
free -m
top
htop
```

---

## 📚 Documentation Commands

### Generate requirements.txt

```bash
pip freeze > requirements.txt
```

### Count Lines of Code

```bash
find . -name "*.py" -exec wc -l {} + | tail -1
```

### Create Project Tree

```bash
tree -L 2 -I 'venv|__pycache__|*.pyc|.git'
```

---

## 🎯 Quick Commands Summary

```bash
# Setup
./setup.sh && source venv/bin/activate

# Load data
python ingest_data.py

# Start server
python app.py

# Test API
curl http://localhost:5000/api/health

# Open dashboard
open http://localhost:5000  # macOS
xdg-open http://localhost:5000  # Linux

# View database
mongosh
use amazon_food_reviews
db.reviews.countDocuments()
```

---

**Keep this file handy for quick reference! 📖✨**
