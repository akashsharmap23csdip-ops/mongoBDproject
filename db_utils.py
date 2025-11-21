"""
Database Utilities and Helper Functions
Provides utility functions for MongoDB operations
"""

from pymongo import MongoClient
import os


def get_mongodb_connection():
    """
    Create and return MongoDB connection
    """
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    return client


def get_collection(database_name=None, collection_name=None):
    """
    Get MongoDB collection
    """
    db_name = database_name or os.getenv('DATABASE_NAME', 'amazon_food_reviews')
    coll_name = collection_name or os.getenv('COLLECTION_NAME', 'reviews')
    
    client = get_mongodb_connection()
    db = client[db_name]
    collection = db[coll_name]
    
    return collection, client


def get_database_stats():
    """
    Get database statistics
    """
    collection, client = get_collection()
    
    stats = {
        'total_documents': collection.count_documents({}),
        'database_name': collection.database.name,
        'collection_name': collection.name,
        'indexes': collection.index_information(),
    }
    
    # Get rating distribution
    rating_dist = {}
    for rating in range(1, 6):
        rating_dist[f'{rating}_stars'] = collection.count_documents({'Rating': rating})
    stats['rating_distribution'] = rating_dist
    
    # Get sentiment statistics
    pipeline = [
        {
            '$group': {
                '_id': None,
                'avg_sentiment': {'$avg': '$sentiment_score'},
                'min_sentiment': {'$min': '$sentiment_score'},
                'max_sentiment': {'$max': '$sentiment_score'}
            }
        }
    ]
    
    sentiment_stats = list(collection.aggregate(pipeline))
    if sentiment_stats:
        stats['sentiment_statistics'] = sentiment_stats[0]
    
    client.close()
    return stats


def clear_collection(database_name=None, collection_name=None):
    """
    Clear all documents from collection
    """
    collection, client = get_collection(database_name, collection_name)
    result = collection.delete_many({})
    client.close()
    return result.deleted_count


def drop_database(database_name=None):
    """
    Drop entire database
    """
    db_name = database_name or os.getenv('DATABASE_NAME', 'amazon_food_reviews')
    client = get_mongodb_connection()
    client.drop_database(db_name)
    client.close()
    return True


if __name__ == "__main__":
    import json
    
    print("="*60)
    print("MongoDB Database Statistics")
    print("="*60)
    
    stats = get_database_stats()
    print(json.dumps(stats, indent=2, default=str))
    
    print("\n" + "="*60)
