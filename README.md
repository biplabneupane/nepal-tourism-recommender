# Nepal Tourism Recommender

A machine learning–based web application for recommending tourist destinations in Nepal based on user preferences.

## Overview

The Nepal Tourism Recommender is a content-based recommendation system designed to suggest suitable travel destinations using user-defined preferences such as interests, budget range, and travel duration. The system analyzes structured destination data, computes similarity scores, and presents the most relevant recommendations through a web interface.

## Features

### Recommendation System
- Content-based recommendation of tourist destinations
- Filtering based on user preferences (category, budget, difficulty)
- Similarity-based recommendations ("Find Similar")
- Preference-based recommendations
- **Explainability**: See why each recommendation was made

### Enhanced User Experience
- **Enhanced recommendation cards** with:
  - Best time to visit
  - Typical trip duration
  - Ideal traveler type
  - Estimated total trip cost
  - Detailed difficulty explanations
- **Trip itinerary generation**: Create multi-day trip plans
- **Preference memory**: System remembers your preferences across sessions

### Conversion & Lead Management
- **Email integration**: Send itineraries directly to users
- **Expert consultation**: Connect users with local travel experts
- **Quote requests**: Request customized pricing
- **Database storage**: All leads and preferences stored persistently
- **Admin dashboard**: View and manage leads via API

### Analytics
- Track recommendation clicks
- Monitor conversions
- Analyze user preferences

## Tech Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy (Database)
- Flask-Mail (Email)

**Machine Learning**
- pandas
- numpy
- scikit-learn

**Frontend**
- HTML
- CSS
- JavaScript (with localStorage for client-side caching)

**Database**
- SQLite (development)
- PostgreSQL compatible (production)


## Methodology

1. User preferences are collected through the web interface.
2. Destination data is processed and represented using feature vectors.
3. A content-based filtering approach computes similarity between user preferences and destinations.
4. The most relevant destinations are returned and displayed to the user.

## License

MIT License
