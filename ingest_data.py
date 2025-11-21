"""
MongoDB Data Ingestion Script for Amazon Food Reviews
Reads CSV, calculates sentiment scores and content length, loads to MongoDB
"""

import pandas as pd
from pymongo import MongoClient
from textblob import TextBlob
import os
from datetime import datetime

# Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'amazon_food_reviews')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'reviews')
CSV_FILE = 'amazon Food Reviews 100k Dataset.csv'


def calculate_sentiment(text):
    """
    Calculate sentiment polarity using TextBlob
    Returns a score between -1 (negative) and +1 (positive)
    """
    try:
        blob = TextBlob(str(text))
        return blob.sentiment.polarity
    except Exception as e:
        print(f"Error calculating sentiment: {e}")
        return 0.0


def preprocess_data(df):
    """
    Preprocess the dataframe by adding sentiment and content length
    """
    print("Calculating sentiment scores and content lengths...")
    
    # Calculate sentiment score for each review
    df['sentiment_score'] = df['Review'].apply(calculate_sentiment)
    
    # Calculate content length (character count)
    df['content_length'] = df['Review'].apply(lambda x: len(str(x)))
    
    # Add metadata
    df['processed_at'] = datetime.utcnow()
    
    # Convert numpy types to native Python types for MongoDB
    df['Id'] = df['Id'].astype(int)
    df['Rating'] = df['Rating'].astype(int)
    df['content_length'] = df['content_length'].astype(int)
    
    return df


def load_to_mongodb(df):
    """
    Load preprocessed data into MongoDB
    """
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Drop existing collection for fresh start
        print(f"Dropping existing collection '{COLLECTION_NAME}' if exists...")
        collection.drop()
        
        # Convert dataframe to dictionary records
        records = df.to_dict('records')
        
        # Insert all documents
        print(f"Inserting {len(records)} documents into MongoDB...")
        result = collection.insert_many(records)
        
        print(f"✓ Successfully inserted {len(result.inserted_ids)} documents!")
        
        # Create indexes for better query performance
        print("Creating indexes...")
        collection.create_index("Rating")
        collection.create_index("sentiment_score")
        collection.create_index("content_length")
        
        print("✓ Indexes created successfully!")
        
        # Print some statistics
        print("\n--- Database Statistics ---")
        print(f"Total documents: {collection.count_documents({})}")
        print(f"Average sentiment score: {df['sentiment_score'].mean():.4f}")
        print(f"Average content length: {df['content_length'].mean():.2f} characters")
        print(f"Rating distribution:")
        for rating in sorted(df['Rating'].unique()):
            count = collection.count_documents({'Rating': int(rating)})
            print(f"  {int(rating)} stars: {count} reviews")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ Error loading data to MongoDB: {e}")
        return False


def main():
    """
    Main function to orchestrate the data ingestion process
    """
    print("="*60)
    print("Amazon Food Reviews - MongoDB Data Ingestion")
    print("="*60)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"✗ Error: CSV file '{CSV_FILE}' not found!")
        return
    
    # Read CSV file
    print(f"\nReading CSV file: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    print(f"✓ Loaded {len(df)} rows from CSV")
    
    # Display sample data
    print("\nSample data (first 3 rows):")
    print(df.head(3))
    
    # Preprocess data
    df = preprocess_data(df)
    print(f"✓ Preprocessing complete!")
    
    # Display preprocessed sample
    print("\nPreprocessed sample (first 3 rows):")
    print(df[['Id', 'Rating', 'sentiment_score', 'content_length']].head(3))
    
    # Load to MongoDB
    success = load_to_mongodb(df)
    
    if success:
        print("\n" + "="*60)
        print("✓ Data ingestion completed successfully!")
        print("="*60)
    else:
        print("\n✗ Data ingestion failed!")


if __name__ == "__main__":
    main()
