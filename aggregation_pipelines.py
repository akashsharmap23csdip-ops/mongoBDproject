"""
MongoDB Aggregation Pipelines for Amazon Food Reviews Analysis
Contains three complex pipelines for sentiment and engagement analysis
"""


def get_sentiment_by_rating_pipeline():
    """
    Pipeline 1: Sentiment by Rating
    Groups reviews by star rating and calculates average sentiment score
    Shows the relationship between star ratings and sentiment polarity
    """
    pipeline = [
        {
            '$group': {
                '_id': '$Rating',
                'avg_sentiment': {'$avg': '$sentiment_score'},
                'review_count': {'$sum': 1},
                'min_sentiment': {'$min': '$sentiment_score'},
                'max_sentiment': {'$max': '$sentiment_score'}
            }
        },
        {
            '$sort': {'_id': 1}
        },
        {
            '$project': {
                '_id': 0,
                'rating': '$_id',
                'avg_sentiment': {'$round': ['$avg_sentiment', 4]},
                'review_count': 1,
                'min_sentiment': {'$round': ['$min_sentiment', 4]},
                'max_sentiment': {'$round': ['$max_sentiment', 4]}
            }
        }
    ]
    return pipeline


def get_content_length_vs_rating_pipeline():
    """
    Pipeline 2: Content Length vs. Rating
    Buckets reviews by content length (Short/Medium/Long) and calculates average rating
    Shows if review length correlates with rating patterns
    """
    pipeline = [
        {
            '$bucket': {
                'groupBy': '$content_length',
                'boundaries': [0, 100, 300, 10000],  # Short: 0-99, Medium: 100-299, Long: 300+
                'default': 'Very Long',
                'output': {
                    'avg_rating': {'$avg': '$Rating'},
                    'review_count': {'$sum': 1},
                    'avg_sentiment': {'$avg': '$sentiment_score'},
                    'avg_length': {'$avg': '$content_length'}
                }
            }
        },
        {
            '$addFields': {
                'length_category': {
                    '$switch': {
                        'branches': [
                            {'case': {'$eq': ['$_id', 0]}, 'then': 'Short (0-99 chars)'},
                            {'case': {'$eq': ['$_id', 100]}, 'then': 'Medium (100-299 chars)'},
                            {'case': {'$eq': ['$_id', 300]}, 'then': 'Long (300+ chars)'}
                        ],
                        'default': 'Very Long'
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'length_category': 1,
                'avg_rating': {'$round': ['$avg_rating', 2]},
                'review_count': 1,
                'avg_sentiment': {'$round': ['$avg_sentiment', 4]},
                'avg_length': {'$round': ['$avg_length', 0]}
            }
        },
        {
            '$sort': {'avg_length': 1}
        }
    ]
    return pipeline


def get_rating_distribution_by_sentiment_pipeline():
    """
    Pipeline 3: Rating Distribution by Sentiment
    Buckets reviews by sentiment (Negative/Neutral/Positive) and shows rating distribution
    Reveals the breakdown of star ratings within each sentiment category
    """
    pipeline = [
        {
            '$bucket': {
                'groupBy': '$sentiment_score',
                'boundaries': [-1.0, -0.1, 0.1, 1.1],  # Negative: -1 to -0.1, Neutral: -0.1 to 0.1, Positive: 0.1+
                'default': 'Neutral',
                'output': {
                    'total_count': {'$sum': 1},
                    'ratings': {
                        '$push': '$Rating'
                    }
                }
            }
        },
        {
            '$addFields': {
                'sentiment_category': {
                    '$switch': {
                        'branches': [
                            {'case': {'$eq': ['$_id', -1.0]}, 'then': 'Negative'},
                            {'case': {'$eq': ['$_id', -0.1]}, 'then': 'Neutral'},
                            {'case': {'$eq': ['$_id', 0.1]}, 'then': 'Positive'}
                        ],
                        'default': 'Neutral'
                    }
                }
            }
        },
        {
            '$unwind': '$ratings'
        },
        {
            '$group': {
                '_id': {
                    'sentiment': '$sentiment_category',
                    'rating': '$ratings'
                },
                'count': {'$sum': 1},
                'total_in_sentiment': {'$first': '$total_count'}
            }
        },
        {
            '$group': {
                '_id': '$_id.sentiment',
                'total_count': {'$first': '$total_in_sentiment'},
                'rating_breakdown': {
                    '$push': {
                        'rating': '$_id.rating',
                        'count': '$count',
                        'percentage': {
                            '$round': [
                                {'$multiply': [
                                    {'$divide': ['$count', '$total_in_sentiment']},
                                    100
                                ]},
                                2
                            ]
                        }
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'sentiment_category': '$_id',
                'total_count': 1,
                'rating_breakdown': 1
            }
        },
        {
            '$sort': {'sentiment_category': 1}
        }
    ]
    return pipeline


def execute_pipeline(collection, pipeline_name):
    """
    Execute a specific aggregation pipeline and return results
    
    Args:
        collection: MongoDB collection object
        pipeline_name: Name of the pipeline to execute
        
    Returns:
        List of aggregation results
    """
    pipelines = {
        'sentiment_by_rating': get_sentiment_by_rating_pipeline(),
        'content_length_vs_rating': get_content_length_vs_rating_pipeline(),
        'rating_distribution_by_sentiment': get_rating_distribution_by_sentiment_pipeline()
    }
    
    if pipeline_name not in pipelines:
        raise ValueError(f"Unknown pipeline: {pipeline_name}")
    
    pipeline = pipelines[pipeline_name]
    results = list(collection.aggregate(pipeline))
    
    return results


# Test function to run pipelines independently
def test_pipelines():
    """
    Test function to run all pipelines and display results
    """
    from pymongo import MongoClient
    import json
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['amazon_food_reviews']
    collection = db['reviews']
    
    print("="*60)
    print("Testing MongoDB Aggregation Pipelines")
    print("="*60)
    
    # Test Pipeline 1
    print("\n1. Sentiment by Rating:")
    print("-" * 40)
    results = execute_pipeline(collection, 'sentiment_by_rating')
    print(json.dumps(results, indent=2))
    
    # Test Pipeline 2
    print("\n2. Content Length vs. Rating:")
    print("-" * 40)
    results = execute_pipeline(collection, 'content_length_vs_rating')
    print(json.dumps(results, indent=2))
    
    # Test Pipeline 3
    print("\n3. Rating Distribution by Sentiment:")
    print("-" * 40)
    results = execute_pipeline(collection, 'rating_distribution_by_sentiment')
    print(json.dumps(results, indent=2))
    
    client.close()
    print("\n" + "="*60)
    print("Pipeline testing complete!")
    print("="*60)


if __name__ == "__main__":
    test_pipelines()
