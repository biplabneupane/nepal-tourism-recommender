from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail
import pandas as pd
import sys
import os
import json
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.recommender.content_based import ContentBasedRecommender
from src.models import db, UserPreference, Lead, ConversionRequest, Analytics
from src.email_service import (
    send_itinerary_email, send_expert_consultation_notification,
    send_quote_request_notification, send_confirmation_email
)
from config import config

app = Flask(__name__)
CORS(app)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Global variables
attractions_df = None
recommender = None


def initialize_system():
    global attractions_df, recommender
    import os
    import pandas as pd

    # Determine absolute path relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, 'data', 'processed', 'attractions.csv')

    print("===== DEBUG =====")
    print("BASE_DIR:", BASE_DIR)
    print("Looking for CSV at:", data_path)
    print("Exists?", os.path.exists(data_path))

    # List directories for debugging
    try:
        print("Contents of BASE_DIR:", os.listdir(BASE_DIR))
        if os.path.exists(os.path.join(BASE_DIR, 'data')):
            print("Contents of data folder:", os.listdir(os.path.join(BASE_DIR, 'data')))
        if os.path.exists(os.path.join(BASE_DIR, 'data', 'processed')):
            print("Contents of processed folder:", os.listdir(os.path.join(BASE_DIR, 'data', 'processed')))
    except Exception as e:
        print("Error listing directories:", e)

    # If CSV not found, fail gracefully
    if not os.path.exists(data_path):
        print("ERROR: CSV file not found! The API will not work.")
        attractions_df = None
        return

    try:
        attractions_df = pd.read_csv(data_path)
        print(f"Loaded {len(attractions_df)} attractions")
    except Exception as e:
        print("ERROR reading CSV:", e)
        attractions_df = None
        return

    try:
        recommender = ContentBasedRecommender()
        recommender.fit(attractions_df)
        print("Model ready!")
    except Exception as e:
        print("ERROR initializing recommender:", e)
        recommender = None


# Initialize database
def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")


# Initialize the system immediately when the module is loaded
# This ensures data loads both in development and production (Gunicorn)
initialize_system()
init_db()


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


@app.route('/api/recommend/explain', methods=['POST'])
def explain_recommendation():
    """Explain why a recommendation was made based on user preferences."""
    try:
        data = request.get_json()
        attraction_id = data.get('attraction_id')
        user_preferences = data.get('preferences', {})
        
        if attraction_id is None:
            return jsonify({
                'success': False,
                'error': 'attraction_id is required'
            }), 400
        
        attraction = attractions_df[attractions_df['attraction_id'] == attraction_id]
        if len(attraction) == 0:
            return jsonify({
                'success': False,
                'error': 'Attraction not found'
            }), 404
        
        attraction = attraction.iloc[0]
        explanations = []
        
        # Check category match
        if user_preferences.get('category'):
            if attraction['category'] == user_preferences['category']:
                explanations.append(f"Matches your interest in {attraction['category']}")
        
        # Check budget match
        if user_preferences.get('max_cost'):
            if attraction['avg_cost_usd'] <= user_preferences['max_cost']:
                explanations.append(f"Fits your budget (${attraction['avg_cost_usd']} < ${user_preferences['max_cost']})")
            else:
                explanations.append(f"Above budget but highly rated option")
        
        # Check difficulty match
        if user_preferences.get('difficulty'):
            if attraction['difficulty'] == user_preferences['difficulty']:
                explanations.append(f"Matches your preferred difficulty level ({attraction['difficulty']})")
        
        # Rating explanation
        if attraction['rating'] >= 4.0:
            explanations.append(f"Highly rated ({attraction['rating']}/5.0) with {attraction['num_reviews']} reviews")
        
        # Season explanation
        explanations.append(f"Best visited in {attraction['best_season']}")
        
        # Default explanation if no specific matches
        if not explanations:
            explanations.append("Popular destination with good ratings")
        
        return jsonify({
            'success': True,
            'explanations': explanations,
            'attraction': {
                'name': attraction['name'],
                'category': attraction['category'],
                'region': attraction['region']
            }
        })
    
    except Exception as e:
        print(f"Error in explain_recommendation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/itinerary/generate', methods=['POST'])
def generate_itinerary():
    """Generate a multi-day itinerary from selected attractions."""
    try:
        data = request.get_json()
        attraction_ids = data.get('attraction_ids', [])
        days = data.get('days', 5)
        start_location = data.get('start_location', 'Kathmandu')
        
        if not attraction_ids:
            return jsonify({
                'success': False,
                'error': 'Please select at least one attraction'
            }), 400
        
        # Get attractions
        selected = attractions_df[attractions_df['attraction_id'].isin(attraction_ids)].copy()
        
        if len(selected) == 0:
            return jsonify({
                'success': False,
                'error': 'Invalid attraction IDs'
            }), 400
        
        # Group by region for logical routing
        selected['region_order'] = selected['region'].map({
            'Kathmandu Valley': 1,
            'Pokhara Region': 2,
            'Everest Region': 3,
            'Annapurna Region': 2,
            'Mustang Region': 4,
            'Langtang Region': 3,
            'Manaslu Region': 3,
            'Chitwan': 5,
            'Lumbini': 5,
            'Far West Nepal': 6
        }).fillna(10)
        
        selected = selected.sort_values(['region_order', 'difficulty', 'duration_days'])
        
        # Build itinerary
        itinerary = []
        current_day = 1
        total_cost = 0
        
        # Add travel days and rest days for difficult treks
        for idx, row in selected.iterrows():
            attraction = row.to_dict()
            
            # For hard/extreme treks, add acclimatization day
            if attraction['difficulty'] in ['Hard', 'Extreme'] and attraction['category'] == 'Trekking':
                days_needed = int(attraction['duration_days']) + 1
            else:
                days_needed = max(1, int(attraction['duration_days']))
            
            if current_day > days:
                break
            
            day_entry = {
                'day': current_day,
                'attraction': {
                    'id': int(attraction['attraction_id']),
                    'name': attraction['name'],
                    'region': attraction['region'],
                    'category': attraction['category']
                },
                'activities': [attraction['name']],
                'duration': days_needed,
                'difficulty': attraction['difficulty'],
                'cost': float(attraction['avg_cost_usd']),
                'best_season': attraction['best_season'],
                'notes': []
            }
            
            # Add notes based on difficulty
            if attraction['difficulty'] in ['Hard', 'Extreme']:
                day_entry['notes'].append(f"Acclimatization recommended for high altitude")
            
            if attraction['category'] == 'Trekking' and days_needed > 3:
                day_entry['notes'].append("Multi-day trek - consider rest day after completion")
            
            itinerary.append(day_entry)
            total_cost += attraction['avg_cost_usd']
            current_day += days_needed
        
        # If itinerary is shorter than requested days, add buffer days
        while current_day <= days and len(itinerary) < days:
            itinerary.append({
                'day': current_day,
                'attraction': None,
                'activities': ['Flexible day - explore local area or rest'],
                'duration': 1,
                'difficulty': 'Easy',
                'cost': 50.0,
                'best_season': 'Year-round',
                'notes': ['Buffer day for rest or spontaneous activities']
            })
            current_day += 1
        
        return jsonify({
            'success': True,
            'itinerary': itinerary,
            'summary': {
                'total_days': min(current_day - 1, days),
                'total_cost': round(total_cost, 2),
                'average_daily_cost': round(total_cost / min(current_day - 1, days), 2),
                'attractions_count': len(selected),
                'regions_covered': selected['region'].unique().tolist()
            }
        })
    
    except Exception as e:
        print(f"Error in generate_itinerary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversion/request', methods=['POST'])
def handle_conversion_request():
    """Handle conversion requests (email, expert consultation, quotes)."""
    try:
        data = request.get_json()
        request_type = data.get('type')  # 'email', 'expert', 'quote'
        user_data = data.get('user_data', {})
        attraction_ids = data.get('attraction_ids', [])
        
        if not request_type:
            return jsonify({
                'success': False,
                'error': 'Request type is required'
            }), 400
        
        # Extract user information
        name = user_data.get('name', user_data.get('email', 'User')).split('@')[0]
        email = user_data.get('email') or user_data.get('contact')
        phone = user_data.get('phone', '')
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email address is required'
            }), 400
        
        # Create lead in database
        lead = Lead(
            name=name,
            email=email,
            phone=phone,
            lead_type=request_type,
            attraction_ids=json.dumps(attraction_ids) if attraction_ids else None,
            metadata=json.dumps(user_data),
            status='new'
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Handle different request types
        email_sent = False
        error_message = None
        
        try:
            if request_type == 'email':
                # Get attraction details for email
                if attraction_ids:
                    selected_attractions = attractions_df[attractions_df['attraction_id'].isin(attraction_ids)]
                    attractions_data = selected_attractions.to_dict('records')
                    
                    # Calculate summary
                    itinerary_summary = {
                        'total_days': int(selected_attractions['duration_days'].sum()),
                        'total_cost': float(selected_attractions['avg_cost_usd'].sum()),
                        'average_daily_cost': float(selected_attractions['avg_cost_usd'].mean()),
                        'attractions_count': len(selected_attractions),
                        'regions_covered': selected_attractions['region'].unique().tolist()
                    }
                    
                    # Send itinerary email
                    email_sent = send_itinerary_email(
                        email, name, attractions_data, itinerary_summary
                    )
                else:
                    email_sent = send_confirmation_email(email, name, 'email')
                
            elif request_type == 'expert':
                # Send confirmation to user
                send_confirmation_email(email, name, 'expert')
                
                # Notify admin
                lead_dict = lead.to_dict()
                lead_dict['contact'] = user_data.get('contact', email)
                email_sent = send_expert_consultation_notification(
                    lead_dict, app.config.get('ADMIN_EMAIL')
                )
                
            elif request_type == 'quote':
                # Send confirmation to user
                send_confirmation_email(email, name, 'quote')
                
                # Notify admin
                lead_dict = lead.to_dict()
                email_sent = send_quote_request_notification(
                    lead_dict, app.config.get('ADMIN_EMAIL')
                )
            
            # Update lead with email status
            if email_sent:
                lead.email_sent = True
                lead.email_sent_at = datetime.utcnow()
                db.session.commit()
            
        except Exception as e:
            error_message = str(e)
            app.logger.error(f"Email sending failed: {error_message}")
        
        # Create conversion request record
        conversion = ConversionRequest(
            lead_id=lead.id,
            request_type=request_type,
            email_to=email,
            status='sent' if email_sent else 'failed',
            error_message=error_message
        )
        if email_sent:
            conversion.sent_at = datetime.utcnow()
        
        db.session.add(conversion)
        db.session.commit()
        
        response_messages = {
            'email': 'Your itinerary has been sent to your email!' if email_sent else 'Your itinerary is being prepared and will be sent shortly!',
            'expert': 'A local travel expert will contact you within 24 hours.',
            'quote': 'A customized quote will be prepared and sent to you within 1-2 business days.'
        }
        
        return jsonify({
            'success': True,
            'message': response_messages.get(request_type, 'Request received successfully'),
            'lead_id': lead.id,
            'email_sent': email_sent,
            'data': {
                'type': request_type,
                'timestamp': datetime.utcnow().isoformat()
            }
        })
    
    except Exception as e:
        app.logger.error(f"Error in handle_conversion_request: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/preferences/save', methods=['POST'])
def save_preferences():
    """Save user preferences to database."""
    try:
        data = request.get_json()
        session_id = data.get('session_id') or request.remote_addr
        email = data.get('email')
        
        # Check if preference exists for this session
        pref = UserPreference.query.filter_by(session_id=session_id).first()
        
        if pref:
            # Update existing
            pref.preferred_category = data.get('category')
            pref.max_cost = data.get('max_cost')
            pref.difficulty = data.get('difficulty')
            pref.preferred_regions = json.dumps(data.get('regions', []))
            pref.visit_count += 1
            pref.updated_at = datetime.utcnow()
            if email:
                pref.user_email = email
        else:
            # Create new
            pref = UserPreference(
                session_id=session_id,
                user_email=email,
                preferred_category=data.get('category'),
                max_cost=data.get('max_cost'),
                difficulty=data.get('difficulty'),
                preferred_regions=json.dumps(data.get('regions', []))
            )
            db.session.add(pref)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'preference_id': pref.id,
            'message': 'Preferences saved successfully'
        })
    
    except Exception as e:
        app.logger.error(f"Error saving preferences: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/preferences/load', methods=['GET'])
def load_preferences():
    """Load user preferences from database."""
    try:
        session_id = request.args.get('session_id') or request.remote_addr
        
        pref = UserPreference.query.filter_by(session_id=session_id).first()
        
        if pref:
            return jsonify({
                'success': True,
                'preferences': pref.to_dict()
            })
        else:
            return jsonify({
                'success': True,
                'preferences': None
            })
    
    except Exception as e:
        app.logger.error(f"Error loading preferences: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all leads (admin endpoint)."""
    try:
        # In production, add authentication here
        status = request.args.get('status', 'all')
        limit = request.args.get('limit', 50, type=int)
        
        query = Lead.query
        
        if status != 'all':
            query = query.filter_by(status=status)
        
        leads = query.order_by(Lead.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'count': len(leads),
            'leads': [lead.to_dict() for lead in leads]
        })
    
    except Exception as e:
        app.logger.error(f"Error getting leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analytics/track', methods=['POST'])
def track_analytics():
    """Track recommendation clicks and conversions."""
    try:
        data = request.get_json()
        
        analytics = Analytics(
            session_id=data.get('session_id') or request.remote_addr,
            recommendation_type=data.get('recommendation_type'),
            attraction_id=data.get('attraction_id'),
            clicked=data.get('clicked', False),
            converted=data.get('converted', False),
            user_preferences=json.dumps(data.get('preferences', {}))
        )
        
        db.session.add(analytics)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Analytics tracked'
        })
    
    except Exception as e:
        app.logger.error(f"Error tracking analytics: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)