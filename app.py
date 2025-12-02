from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.recommender.content_based import ContentBasedRecommender

app = Flask(__name__)
CORS(app)

# Global variables
attractions_df = None
recommender = None


def initialize_system():
    """Load data and train model at startup."""
    global attractions_df, recommender
    
    print("Loading data and training model...")
    try:
        attractions_df = pd.read_csv('data/processed/attractions.csv')
        print(f"Loaded {len(attractions_df)} attractions")
        
        recommender = ContentBasedRecommender()
        recommender.fit(attractions_df)
        print("Model ready!")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find attractions.csv - {e}")
        print("Please make sure the file is at: data/processed/attractions.csv")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing system: {e}")
        sys.exit(1)


@app.route('/')
def home():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/attractions', methods=['GET'])
def get_all_attractions():
    """Get all attractions with optional filters."""
    try:
        df = attractions_df.copy()
        
        # Apply filters if provided
        category = request.args.get('category')
        region = request.args.get('region')
        max_cost = request.args.get('max_cost', type=int)
        min_rating = request.args.get('min_rating', type=float)
        
        if category:
            df = df[df['category'] == category]
        if region:
            df = df[df['region'] == region]
        if max_cost:
            df = df[df['avg_cost_usd'] <= max_cost]
        if min_rating:
            df = df[df['rating'] >= min_rating]
        
        # Sort by rating
        df = df.sort_values('rating', ascending=False)
        
        return jsonify({
            'success': True,
            'count': len(df),
            'attractions': df.to_dict('records')
        })
    
    except Exception as e:
        print(f"Error in get_all_attractions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/attraction/<int:attraction_id>', methods=['GET'])
def get_attraction(attraction_id):
    """Get details of a specific attraction."""
    try:
        attraction = attractions_df[attractions_df['attraction_id'] == attraction_id]
        
        if len(attraction) == 0:
            return jsonify({
                'success': False,
                'error': 'Attraction not found'
            }), 404
        
        return jsonify({
            'success': True,
            'attraction': attraction.iloc[0].to_dict()
        })
    
    except Exception as e:
        print(f"Error in get_attraction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommend/similar/<int:attraction_id>', methods=['GET'])
def recommend_similar(attraction_id):
    """Get recommendations similar to a specific attraction."""
    try:
        top_n = request.args.get('top_n', default=5, type=int)
        
        # Get recommendations
        recommendations = recommender.recommend(
            attraction_id=attraction_id,
            top_n=top_n
        )
        
        # Get original attraction
        original = attractions_df[attractions_df['attraction_id'] == attraction_id].iloc[0]
        
        return jsonify({
            'success': True,
            'original': {
                'id': int(original['attraction_id']),
                'name': original['name'],
                'category': original['category'],
                'region': original['region']
            },
            'recommendations': recommendations.to_dict('records')
        })
    
    except ValueError as e:
        print(f"ValueError in recommend_similar: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        print(f"Error in recommend_similar: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommend/preferences', methods=['POST'])
def recommend_by_preferences():
    """Get recommendations based on user preferences."""
    try:
        data = request.get_json()
        
        category = data.get('category')
        max_cost = data.get('max_cost')
        difficulty = data.get('difficulty')
        top_n = data.get('top_n', 10)
        
        recommendations = recommender.recommend_by_preferences(
            preferred_category=category if category else None,
            max_cost=max_cost if max_cost else None,
            difficulty=difficulty if difficulty else None,
            top_n=top_n
        )
        
        return jsonify({
            'success': True,
            'count': len(recommendations),
            'recommendations': recommendations.to_dict('records')
        })
    
    except Exception as e:
        print(f"Error in recommend_by_preferences: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics."""
    try:
        stats = {
            'total_attractions': int(len(attractions_df)),
            'categories': {k: int(v) for k, v in attractions_df['category'].value_counts().to_dict().items()},
            'regions': {k: int(v) for k, v in attractions_df['region'].value_counts().to_dict().items()},
            'avg_rating': float(attractions_df['rating'].mean()),
            'avg_cost': float(attractions_df['avg_cost_usd'].mean()),
            'cost_range': {
                'min': float(attractions_df['avg_cost_usd'].min()),
                'max': float(attractions_df['avg_cost_usd'].max())
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    initialize_system()
    app.run(debug=True, host='0.0.0.0', port=5000)