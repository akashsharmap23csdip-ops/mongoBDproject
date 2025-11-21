"""
Flask API Backend for Amazon Food Reviews Analysis
Provides three API endpoints that execute MongoDB aggregation pipelines
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os
from aggregation_pipelines import execute_pipeline

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'amazon_food_reviews')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'reviews')

# Initialize MongoDB connection
client = None
collection = None


def get_collection():
    """
    Get MongoDB collection with lazy initialization
    """
    global client, collection
    if collection is None:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
    return collection


@app.route('/')
def index():
    """
    Serve the main dashboard HTML page
    """
    return render_template('dashboard.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API and database connectivity
    """
    try:
        coll = get_collection()
        total_reviews = coll.count_documents({})
        return jsonify({
            'status': 'healthy',
            'database': DATABASE_NAME,
            'collection': COLLECTION_NAME,
            'total_reviews': total_reviews
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/sentiment_by_rating', methods=['GET'])
def sentiment_by_rating():
    """
    API Endpoint 1: Sentiment by Rating
    Returns average sentiment scores grouped by star ratings
    """
    try:
        coll = get_collection()
        results = execute_pipeline(coll, 'sentiment_by_rating')
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/content_length_vs_rating', methods=['GET'])
def content_length_vs_rating():
    """
    API Endpoint 2: Content Length vs. Rating
    Returns average ratings grouped by review content length categories
    """
    try:
        coll = get_collection()
        results = execute_pipeline(coll, 'content_length_vs_rating')
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rating_distribution_by_sentiment', methods=['GET'])
def rating_distribution_by_sentiment():
    """
    API Endpoint 3: Rating Distribution by Sentiment
    Returns the breakdown of star ratings within each sentiment category
    """
    try:
        coll = get_collection()
        results = execute_pipeline(coll, 'rating_distribution_by_sentiment')
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/all_analytics', methods=['GET'])
def all_analytics():
    """
    Bonus endpoint: Returns all three analytics in a single call
    Useful for dashboard initialization
    """
    try:
        coll = get_collection()
        
        # Execute all three pipelines
        sentiment_data = execute_pipeline(coll, 'sentiment_by_rating')
        length_data = execute_pipeline(coll, 'content_length_vs_rating')
        distribution_data = execute_pipeline(coll, 'rating_distribution_by_sentiment')
        
        # Get total review count
        total_reviews = coll.count_documents({})
        
        return jsonify({
            'success': True,
            'total_reviews': total_reviews,
            'analytics': {
                'sentiment_by_rating': sentiment_data,
                'content_length_vs_rating': length_data,
                'rating_distribution_by_sentiment': distribution_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


def shutdown_db():
    """
    Close MongoDB connection on app shutdown
    """
    global client
    if client:
        client.close()


if __name__ == '__main__':
    import atexit
    atexit.register(shutdown_db)
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("="*60)
    print("Amazon Food Reviews - Analytics API Server")
    print("="*60)
    print(f"Database: {DATABASE_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Server: http://{host}:{port}")
    print("\nAvailable Endpoints:")
    print(f"  GET /api/health")
    print(f"  GET /api/sentiment_by_rating")
    print(f"  GET /api/content_length_vs_rating")
    print(f"  GET /api/rating_distribution_by_sentiment")
    print(f"  GET /api/all_analytics")
    print("="*60)
    
    app.run(host=host, port=port, debug=debug)
