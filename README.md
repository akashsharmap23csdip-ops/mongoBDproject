# 🍎 MongoDB-based Customer Sentiment and Engagement Analysis of Amazon Food Reviews

A comprehensive data analytics project that leverages MongoDB's aggregation framework to analyze 100,000 Amazon food reviews, performing sentiment analysis and engagement metrics visualization through an interactive web dashboard.

![Project Banner](https://img.shields.io/badge/MongoDB-Analysis-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [MongoDB Aggregation Pipelines](#mongodb-aggregation-pipelines)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

This project demonstrates advanced MongoDB aggregation techniques combined with sentiment analysis to extract meaningful insights from a large dataset of Amazon food reviews. It showcases:

- **Big Data Processing**: Handling 100,000+ reviews efficiently
- **Sentiment Analysis**: Using TextBlob to calculate polarity scores
- **Complex Aggregations**: Three sophisticated MongoDB pipelines
- **RESTful API**: Flask backend with multiple analytical endpoints
- **Interactive Visualization**: Real-time dashboard with Chart.js

### Key Insights Provided

1. **Sentiment by Rating**: Correlation between star ratings and sentiment polarity
2. **Content Length Analysis**: Relationship between review length and ratings
3. **Sentiment Distribution**: How star ratings break down within sentiment categories

## ✨ Features

- 📊 **Real-time Analytics Dashboard** - Interactive visualizations updated from MongoDB
- 🧠 **Automated Sentiment Analysis** - TextBlob-powered sentiment scoring
- 🔄 **Complex Aggregation Pipelines** - Advanced MongoDB queries with grouping, bucketing, and projections
- 🚀 **RESTful API** - Clean Flask endpoints for data access
- 📈 **Multiple Chart Types** - Bar charts, stacked charts for comprehensive analysis
- 💾 **Efficient Data Storage** - Indexed MongoDB collections for fast queries
- 🎨 **Responsive Design** - Mobile-friendly dashboard interface

## 🏗️ Architecture

```
┌─────────────────┐
│   CSV Dataset   │
│  (100K Reviews) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Ingestion │
│   (TextBlob +   │
│    Pandas)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    MongoDB      │
│   Collection    │
│  (Indexed)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Aggregation    │
│   Pipelines     │
│  (3 Complex)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │
│  (REST Endpoints)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│  (Chart.js UI)  │
└─────────────────┘
```

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **MongoDB 4.4+** (running locally or accessible remotely)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Installing MongoDB

**Ubuntu/Debian:**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
Download from [MongoDB Official Website](https://www.mongodb.com/try/download/community)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mongoBDproject.git
cd mongoBDproject
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

### 5. Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your MongoDB connection details if needed
```

## 🚀 Usage

### Phase 1: Data Ingestion

Load the Amazon Food Reviews dataset into MongoDB with sentiment analysis:

```bash
python ingest_data.py
```

**Expected Output:**
```
============================================================
Amazon Food Reviews - MongoDB Data Ingestion
============================================================

Reading CSV file: amazon Food Reviews 100k Dataset.csv
✓ Loaded 100000 rows from CSV
Calculating sentiment scores and content lengths...
✓ Preprocessing complete!
Connecting to MongoDB at mongodb://localhost:27017/...
✓ Successfully inserted 100000 documents!
✓ Indexes created successfully!

--- Database Statistics ---
Total documents: 100000
Average sentiment score: 0.2845
Average content length: 342.56 characters
```

**This step:**
- Reads the CSV file
- Calculates sentiment score for each review using TextBlob
- Calculates content length (character count)
- Inserts all documents into MongoDB
- Creates indexes for optimized queries

### Phase 2: Test Aggregation Pipelines (Optional)

Test the MongoDB pipelines independently:

```bash
python aggregation_pipelines.py
```

### Phase 3: Start the Flask API Server

```bash
python app.py
```

**Expected Output:**
```
============================================================
Amazon Food Reviews - Analytics API Server
============================================================
Database: amazon_food_reviews
Collection: reviews
Server: http://0.0.0.0:5000

Available Endpoints:
  GET /api/health
  GET /api/sentiment_by_rating
  GET /api/content_length_vs_rating
  GET /api/rating_distribution_by_sentiment
  GET /api/all_analytics
============================================================
```

### Phase 4: Access the Dashboard

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the **Amazon Food Review Analysis Dashboard** with three interactive charts.

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "amazon_food_reviews",
  "collection": "reviews",
  "total_reviews": 100000
}
```

#### 2. Sentiment by Rating
```http
GET /api/sentiment_by_rating
```

**Description:** Returns average sentiment scores grouped by star ratings (1-5).

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "rating": 1,
      "avg_sentiment": -0.2453,
      "review_count": 8234,
      "min_sentiment": -1.0,
      "max_sentiment": 0.8
    },
    ...
  ],
  "count": 5
}
```

#### 3. Content Length vs Rating
```http
GET /api/content_length_vs_rating
```

**Description:** Returns average ratings grouped by review length categories.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "length_category": "Short (0-99 chars)",
      "avg_rating": 4.12,
      "review_count": 12543,
      "avg_sentiment": 0.2134,
      "avg_length": 67
    },
    ...
  ],
  "count": 3
}
```

#### 4. Rating Distribution by Sentiment
```http
GET /api/rating_distribution_by_sentiment
```

**Description:** Returns the breakdown of star ratings within each sentiment category.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "sentiment_category": "Negative",
      "total_count": 15234,
      "rating_breakdown": [
        {"rating": 1, "count": 8234, "percentage": 54.03},
        {"rating": 2, "count": 4567, "percentage": 29.97},
        ...
      ]
    },
    ...
  ],
  "count": 3
}
```

#### 5. All Analytics (Bonus)
```http
GET /api/all_analytics
```

**Description:** Returns all three analytics in a single call.

**Response:**
```json
{
  "success": true,
  "total_reviews": 100000,
  "analytics": {
    "sentiment_by_rating": [...],
    "content_length_vs_rating": [...],
    "rating_distribution_by_sentiment": [...]
  }
}
```

## 🔍 MongoDB Aggregation Pipelines

### Pipeline 1: Sentiment by Rating

**Purpose:** Groups reviews by star rating and calculates average sentiment score.

**Pipeline Stages:**
1. `$group` - Groups by rating, calculates avg/min/max sentiment
2. `$sort` - Sorts by rating ascending
3. `$project` - Formats output with rounded values

**Key Operations:**
- `$avg` - Average sentiment calculation
- `$min/$max` - Range of sentiments per rating
- `$round` - Precision formatting

### Pipeline 2: Content Length vs Rating

**Purpose:** Buckets reviews by content length and shows average rating per bucket.

**Pipeline Stages:**
1. `$bucket` - Creates three buckets: Short (0-99), Medium (100-299), Long (300+)
2. `$addFields` - Adds human-readable category labels
3. `$project` - Formats output
4. `$sort` - Orders by length

**Key Operations:**
- `$bucket` - Automatic bucketing by content_length
- `$switch` - Conditional category naming
- `$avg` - Multiple averages (rating, sentiment, length)

### Pipeline 3: Rating Distribution by Sentiment

**Purpose:** Buckets by sentiment category and shows rating distribution within each.

**Pipeline Stages:**
1. `$bucket` - Creates sentiment buckets: Negative (-1 to -0.1), Neutral (-0.1 to 0.1), Positive (0.1+)
2. `$addFields` - Labels sentiment categories
3. `$unwind` - Explodes ratings array
4. `$group` (nested) - Groups by sentiment and rating
5. `$group` (final) - Aggregates rating breakdowns
6. `$project` - Final formatting
7. `$sort` - Orders output

**Key Operations:**
- `$bucket` - Sentiment categorization
- `$push` - Collects ratings into arrays
- `$unwind` - Array deconstruction
- Nested `$group` - Multi-level aggregation
- Percentage calculations

## 📁 Project Structure

```
mongoBDproject/
│
├── amazon Food Reviews 100k Dataset.csv    # Dataset (100K reviews)
├── amazon Food Reviews 100k Dataset.csv.zip
│
├── ingest_data.py                          # Phase 2: Data ingestion script
├── aggregation_pipelines.py               # Phase 3: MongoDB pipeline definitions
├── app.py                                  # Phase 4: Flask API backend
│
├── templates/
│   └── dashboard.html                      # Phase 5: Web dashboard UI
│
├── requirements.txt                        # Python dependencies
├── .env.example                            # Environment configuration template
├── .gitignore                              # Git ignore rules
├── README.md                               # This file
└── information                             # Project specification
```

## 🛠️ Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0** - Web framework for API
- **PyMongo 4.6** - MongoDB driver for Python
- **Pandas 2.1** - Data manipulation and CSV processing
- **TextBlob 0.17** - Natural language processing for sentiment analysis

### Database
- **MongoDB 4.4+** - NoSQL database with aggregation framework

### Frontend
- **HTML5/CSS3** - Dashboard structure and styling
- **JavaScript (ES6+)** - Client-side logic
- **Chart.js 4.4** - Data visualization library

### Development
- **Git** - Version control
- **Virtual Environment** - Dependency isolation

## 🎨 Dashboard Features

### Visual Components

1. **Header Section**
   - Project title and description
   - Clean, professional design

2. **Statistics Cards**
   - Total reviews analyzed
   - Average sentiment score
   - Most common rating

3. **Chart 1: Sentiment by Rating** (Bar Chart)
   - X-axis: Star ratings (1-5)
   - Y-axis: Sentiment score (-1 to +1)
   - Color-coded bars for visual distinction

4. **Chart 2: Content Length vs Rating** (Bar Chart)
   - X-axis: Length categories (Short/Medium/Long)
   - Y-axis: Average star rating
   - Shows engagement patterns

5. **Chart 3: Rating Distribution** (Stacked Bar Chart)
   - X-axis: Sentiment categories (Negative/Neutral/Positive)
   - Y-axis: Count of reviews
   - Stacked by star rating (1-5)
   - Reveals nuanced patterns

### Interactive Features
- Hover tooltips with detailed information
- Responsive design for mobile devices
- Real-time data loading from API
- Error handling and loading states

## 🧪 Testing

### Manual Testing

1. **Test Data Ingestion:**
   ```bash
   python ingest_data.py
   ```
   Verify: Check MongoDB for 100,000 documents

2. **Test Pipelines:**
   ```bash
   python aggregation_pipelines.py
   ```
   Verify: JSON output for all three pipelines

3. **Test API Endpoints:**
   ```bash
   # Start server
   python app.py
   
   # In another terminal, test endpoints:
   curl http://localhost:5000/api/health
   curl http://localhost:5000/api/sentiment_by_rating
   curl http://localhost:5000/api/content_length_vs_rating
   curl http://localhost:5000/api/rating_distribution_by_sentiment
   ```

4. **Test Dashboard:**
   Open `http://localhost:5000` in browser and verify all charts load

### MongoDB Verification

```bash
# Connect to MongoDB
mongosh

# Use database
use amazon_food_reviews

# Check document count
db.reviews.countDocuments()

# Sample document
db.reviews.findOne()

# Check indexes
db.reviews.getIndexes()
```

## 🔧 Troubleshooting

### Common Issues

**1. MongoDB Connection Error**
```
Error: MongoServerError: connect ECONNREFUSED
```
**Solution:** Ensure MongoDB is running:
```bash
sudo systemctl status mongodb  # Linux
brew services list              # macOS
```

**2. TextBlob Import Error**
```
LookupError: Resource punkt not found
```
**Solution:** Download TextBlob corpora:
```bash
python -m textblob.download_corpora
```

**3. Port Already in Use**
```
OSError: [Errno 98] Address already in use
```
**Solution:** Change port in `.env` or kill existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

**4. Dataset Not Found**
```
Error: CSV file 'amazon Food Reviews 100k Dataset.csv' not found!
```
**Solution:** Extract the zip file:
```bash
unzip "amazon Food Reviews 100k Dataset.csv.zip"
```

## 📈 Performance Considerations

- **Indexes**: Automatically created on Rating, sentiment_score, and content_length
- **Batch Insert**: Uses `insert_many()` for efficient bulk loading
- **Aggregation Optimization**: Pipelines use `$project` to limit returned fields
- **Connection Pooling**: PyMongo handles connection pooling automatically

## 🚀 Future Enhancements

- [ ] Add user authentication for dashboard
- [ ] Implement real-time data updates (WebSockets)
- [ ] Add more advanced NLP analysis (named entity recognition)
- [ ] Create export functionality (PDF reports)
- [ ] Add filtering and date range selection
- [ ] Implement caching layer (Redis)
- [ ] Add unit and integration tests
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Add more visualization types (word clouds, heatmaps)
- [ ] Implement A/B testing insights

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

## 🙏 Acknowledgments

- Amazon for the food reviews dataset
- MongoDB for the powerful aggregation framework
- TextBlob for sentiment analysis capabilities
- Chart.js for beautiful visualizations
- Flask community for excellent documentation

---

**Built with ❤️ using MongoDB, Python, and Flask**
