import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)


def generate_attractions_data(num_attractions=50):

    print(f"  Generating {num_attractions} attractions...")
    
    # Comprehensive mapping of attractions with correct region, category, and difficulty
    attraction_mapping = {
        # Famous treks
        'Mount Everest Base Camp Trek': {
            'region': 'Everest Region',
            'category': 'Trekking',
            'difficulty': 'Hard',
            'duration': 12,
            'cost_range': (1200, 1500),
            'altitude_range': (4000, 5500),
            'best_season': 'Spring'
        },
        'Annapurna Circuit': {
            'region': 'Annapurna Region',
            'category': 'Trekking',
            'difficulty': 'Moderate-Hard',
            'duration': 14,
            'cost_range': (1000, 1400),
            'altitude_range': (2000, 5400),
            'best_season': 'Autumn'
        },
        'Langtang Trek': {
            'region': 'Langtang Region',
            'category': 'Trekking',
            'difficulty': 'Moderate',
            'duration': 8,
            'cost_range': (800, 1100),
            'altitude_range': (2000, 3800),
            'best_season': 'Autumn'
        },
        'Manaslu Circuit': {
            'region': 'Manaslu Region',
            'category': 'Trekking',
            'difficulty': 'Hard',
            'duration': 18,
            'cost_range': (1200, 1500),
            'altitude_range': (2000, 5100),
            'best_season': 'Spring'
        },
        'Upper Mustang Trek': {
            'region': 'Mustang Region',
            'category': 'Trekking',
            'difficulty': 'Moderate-Hard',
            'duration': 14,
            'cost_range': (1000, 1400),
            'altitude_range': (2500, 4200),
            'best_season': 'Autumn'
        },
        'Gokyo Lakes Trek': {
            'region': 'Everest Region',
            'category': 'Trekking',
            'difficulty': 'Hard',
            'duration': 14,
            'cost_range': (1200, 1500),
            'altitude_range': (4000, 5400),
            'best_season': 'Spring'
        },
        'Annapurna Base Camp': {
            'region': 'Annapurna Region',
            'category': 'Trekking',
            'difficulty': 'Moderate-Hard',
            'duration': 12,
            'cost_range': (1000, 1400),
            'altitude_range': (2000, 4100),
            'best_season': 'Autumn'
        },
        'Ghandruk Village': {
            'region': 'Annapurna Region',
            'category': 'Trekking',
            'difficulty': 'Moderate',
            'duration': 4,
            'cost_range': (300, 600),
            'altitude_range': (2000, 2200),
            'best_season': 'Autumn'
        },
        'Australian Camp': {
            'region': 'Pokhara Region',
            'category': 'Trekking',
            'difficulty': 'Easy-Moderate',
            'duration': 2,
            'cost_range': (200, 400),
            'altitude_range': (1500, 2000),
            'best_season': 'Year-round'
        },
        'Dhulikhel': {
            'region': 'Kathmandu Valley',
            'category': 'Hill Station',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (1500, 1600),
            'best_season': 'Year-round'
        },
        
        # Cultural sites
        'Kathmandu Durbar Square': {
            'region': 'Kathmandu Valley',
            'category': 'Cultural Heritage',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (20, 40),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Patan Durbar Square': {
            'region': 'Kathmandu Valley',
            'category': 'Cultural Heritage',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (15, 35),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Bhaktapur Durbar Square': {
            'region': 'Kathmandu Valley',
            'category': 'Cultural Heritage',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (15, 35),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Lukla Airport Experience': {
            'region': 'Everest Region',
            'category': 'Adventure Sports',
            'difficulty': 'Moderate',
            'duration': 1,
            'cost_range': (100, 200),
            'altitude_range': (2800, 2900),
            'best_season': 'Year-round'
        },
        
        # Religious sites
        'Swayambhunath (Monkey Temple)': {
            'region': 'Kathmandu Valley',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Boudhanath Stupa': {
            'region': 'Kathmandu Valley',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Pashupatinath Temple': {
            'region': 'Kathmandu Valley',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 20),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        'Lumbini (Buddha Birthplace)': {
            'region': 'Lumbini',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 20),
            'altitude_range': (100, 200),
            'best_season': 'Year-round'
        },
        'Muktinath Temple': {
            'region': 'Mustang Region',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (3700, 3800),
            'best_season': 'Year-round'
        },
        'Tengboche Monastery': {
            'region': 'Everest Region',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (3800, 3900),
            'best_season': 'Year-round'
        },
        'Tal Barahi Temple': {
            'region': 'Pokhara Region',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        'Janakpur Temple': {
            'region': 'Lumbini',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 20),
            'altitude_range': (100, 200),
            'best_season': 'Year-round'
        },
        'Kopan Monastery': {
            'region': 'Kathmandu Valley',
            'category': 'Religious Site',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (5, 15),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        
        # Natural attractions
        'Pokhara Lakeside': {
            'region': 'Pokhara Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 2,
            'cost_range': (100, 250),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        'Chitwan National Park': {
            'region': 'Chitwan',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy-Moderate',
            'duration': 3,
            'cost_range': (200, 500),
            'altitude_range': (100, 200),
            'best_season': 'Winter'
        },
        'Rara Lake': {
            'region': 'Far West Nepal',
            'category': 'Nature & Wildlife',
            'difficulty': 'Moderate-Hard',
            'duration': 7,
            'cost_range': (400, 800),
            'altitude_range': (2900, 3000),
            'best_season': 'Autumn'
        },
        'Phewa Lake': {
            'region': 'Pokhara Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        'Begnas Lake': {
            'region': 'Pokhara Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (600, 700),
            'best_season': 'Year-round'
        },
        'Gosaikunda Lake': {
            'region': 'Langtang Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Moderate-Hard',
            'duration': 4,
            'cost_range': (300, 600),
            'altitude_range': (4000, 4400),
            'best_season': 'Summer'
        },
        'Tilicho Lake': {
            'region': 'Annapurna Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Hard',
            'duration': 8,
            'cost_range': (600, 1000),
            'altitude_range': (4800, 5000),
            'best_season': 'Autumn'
        },
        'Bardiya National Park': {
            'region': 'Far West Nepal',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy-Moderate',
            'duration': 3,
            'cost_range': (200, 500),
            'altitude_range': (100, 200),
            'best_season': 'Winter'
        },
        'Koshi Tappu Wildlife Reserve': {
            'region': 'Lumbini',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 2,
            'cost_range': (100, 300),
            'altitude_range': (100, 200),
            'best_season': 'Winter'
        },
        'Seti River Gorge': {
            'region': 'Pokhara Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        
        # Hill stations
        'Nagarkot Hill Station': {
            'region': 'Kathmandu Valley',
            'category': 'Hill Station',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (2100, 2200),
            'best_season': 'Year-round'
        },
        'Bandipur Village': {
            'region': 'Pokhara Region',
            'category': 'Hill Station',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 200),
            'altitude_range': (1000, 1100),
            'best_season': 'Year-round'
        },
        'Sarangkot Sunrise Point': {
            'region': 'Pokhara Region',
            'category': 'Hill Station',
            'difficulty': 'Easy-Moderate',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (1500, 1600),
            'best_season': 'Year-round'
        },
        
        # Adventure
        'Bungee Jumping (The Last Resort)': {
            'region': 'Kathmandu Valley',
            'category': 'Adventure Sports',
            'difficulty': 'Hard',
            'duration': 1,
            'cost_range': (80, 120),
            'altitude_range': (100, 200),
            'best_season': 'Year-round'
        },
        'Paragliding in Pokhara': {
            'region': 'Pokhara Region',
            'category': 'Adventure Sports',
            'difficulty': 'Moderate',
            'duration': 1,
            'cost_range': (80, 150),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        'White Water Rafting Trishuli': {
            'region': 'Kathmandu Valley',
            'category': 'Adventure Sports',
            'difficulty': 'Moderate',
            'duration': 1,
            'cost_range': (50, 100),
            'altitude_range': (500, 600),
            'best_season': 'Year-round'
        },
        'Poon Hill Sunrise': {
            'region': 'Annapurna Region',
            'category': 'Adventure Sports',
            'difficulty': 'Easy-Moderate',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (3100, 3200),
            'best_season': 'Spring'
        },
        'World Peace Pagoda': {
            'region': 'Pokhara Region',
            'category': 'Adventure Sports',
            'difficulty': 'Easy-Moderate',
            'duration': 1,
            'cost_range': (50, 100),
            'altitude_range': (1100, 1200),
            'best_season': 'Year-round'
        },
        
        # Markets and shopping
        'Namche Bazaar Market': {
            'region': 'Everest Region',
            'category': 'Market/Shopping',
            'difficulty': 'Easy',
            'duration': 0.5,
            'cost_range': (20, 100),
            'altitude_range': (3400, 3500),
            'best_season': 'Year-round'
        },
        'Khumjung Village': {
            'region': 'Everest Region',
            'category': 'Market/Shopping',
            'difficulty': 'Easy',
            'duration': 0.5,
            'cost_range': (20, 80),
            'altitude_range': (3700, 3800),
            'best_season': 'Year-round'
        },
        'Jomsom Town': {
            'region': 'Mustang Region',
            'category': 'Market/Shopping',
            'difficulty': 'Easy',
            'duration': 0.5,
            'cost_range': (20, 100),
            'altitude_range': (2700, 2800),
            'best_season': 'Year-round'
        },
        'Thamel Market': {
            'region': 'Kathmandu Valley',
            'category': 'Market/Shopping',
            'difficulty': 'Easy',
            'duration': 0.5,
            'cost_range': (20, 100),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
        
        # Other attractions
        'Everest View Hotel': {
            'region': 'Everest Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (100, 200),
            'altitude_range': (3800, 3900),
            'best_season': 'Year-round'
        },
        'Kagbeni Village': {
            'region': 'Mustang Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (50, 150),
            'altitude_range': (2800, 2900),
            'best_season': 'Year-round'
        },
        'Mahendra Cave': {
            'region': 'Pokhara Region',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (20, 50),
            'altitude_range': (800, 900),
            'best_season': 'Year-round'
        },
        'Garden of Dreams': {
            'region': 'Kathmandu Valley',
            'category': 'Nature & Wildlife',
            'difficulty': 'Easy',
            'duration': 1,
            'cost_range': (10, 30),
            'altitude_range': (1300, 1400),
            'best_season': 'Year-round'
        },
    }
    
    # Real Nepal destinations (base list)
    base_attractions = [
        # Famous treks
        'Mount Everest Base Camp Trek',
        'Annapurna Circuit',
        'Langtang Trek',
        'Manaslu Circuit',
        'Upper Mustang Trek',
        'Gokyo Lakes Trek',
        
        # Cultural sites
        'Kathmandu Durbar Square',
        'Patan Durbar Square',
        'Bhaktapur Durbar Square',
        
        # Religious sites
        'Swayambhunath (Monkey Temple)',
        'Boudhanath Stupa',
        'Pashupatinath Temple',
        'Lumbini (Buddha Birthplace)',
        
        # Natural attractions
        'Pokhara Lakeside',
        'Chitwan National Park',
        'Rara Lake',
        'Phewa Lake',
        'Begnas Lake',
        
        # Hill stations
        'Nagarkot Hill Station',
        'Dhulikhel',
        'Bandipur Village',
        
        # Adventure
        'Bungee Jumping (The Last Resort)',
        'Paragliding in Pokhara',
        'White Water Rafting Trishuli',
        
        # More destinations
        'Gosaikunda Lake',
        'Tilicho Lake',
        'Janakpur Temple',
        'Bardiya National Park',
        'Koshi Tappu Wildlife Reserve',
    ]
    
    # Adding more generic attractions
    additional_names = [
        'Namche Bazaar Market',
        'Tengboche Monastery',
        'Khumjung Village',
        'Lukla Airport Experience',
        'Everest View Hotel',
        'Annapurna Base Camp',
        'Poon Hill Sunrise',
        'Muktinath Temple',
        'Kagbeni Village',
        'Jomsom Town',
        'Ghandruk Village',
        'Australian Camp',
        'Sarangkot Sunrise Point',
        'World Peace Pagoda',
        'Mahendra Cave',
        'Seti River Gorge',
        'Tal Barahi Temple',
        'Garden of Dreams',
        'Thamel Market',
        'Kopan Monastery'
    ]
    
    all_attractions = base_attractions + additional_names
    
    # Only using the needed number
    selected_attractions = all_attractions[:num_attractions]
    
    difficulties = ['Easy', 'Easy-Moderate', 'Moderate', 'Moderate-Hard', 'Hard', 'Extreme']
    
    attractions = []
    
    for i, name in enumerate(selected_attractions):
        
        # Check if we have a specific mapping for this attraction
        if name in attraction_mapping:
            mapping = attraction_mapping[name]
            region = mapping['region']
            category = mapping['category']
            difficulty = mapping['difficulty']
            duration = mapping['duration']
            cost = np.random.randint(mapping['cost_range'][0], mapping['cost_range'][1])
            altitude = np.random.randint(mapping['altitude_range'][0], mapping['altitude_range'][1])
            best_season = mapping['best_season']
        else:
            # Fallback to generic logic for unmapped attractions
            if any(word in name.lower() for word in ['trek', 'circuit', 'base camp', 'hike']):
                category = 'Trekking'
                difficulty = np.random.choice(['Moderate', 'Moderate-Hard', 'Hard', 'Extreme'])
                duration = np.random.randint(7, 21)
                cost = np.random.randint(500, 1500)
                best_season = np.random.choice(['Spring', 'Autumn'])
                altitude = np.random.randint(2000, 4500)
                
            elif any(word in name.lower() for word in ['temple', 'stupa', 'monastery', 'lumbini']):
                category = 'Religious Site'
                difficulty = 'Easy'
                duration = 1
                cost = np.random.randint(10, 50)
                best_season = 'Year-round'
                altitude = np.random.randint(500, 2000)
                
            elif any(word in name.lower() for word in ['lake', 'river', 'waterfall']):
                category = 'Nature & Wildlife'
                difficulty = np.random.choice(['Easy', 'Moderate', 'Hard'])
                duration = np.random.randint(1, 7)
                cost = np.random.randint(50, 400)
                best_season = np.random.choice(['Spring', 'Summer', 'Autumn'])
                altitude = np.random.randint(500, 2000)
                
            elif any(word in name.lower() for word in ['durbar square', 'palace', 'historic']):
                category = 'Cultural Heritage'
                difficulty = 'Easy'
                duration = 1
                cost = np.random.randint(15, 40)
                best_season = 'Year-round'
                altitude = np.random.randint(500, 2000)
                
            elif any(word in name.lower() for word in ['paragliding', 'bungee', 'rafting']):
                category = 'Adventure Sports'
                difficulty = np.random.choice(['Moderate', 'Hard'])
                duration = 1
                cost = np.random.randint(80, 200)
                best_season = np.random.choice(['Spring', 'Autumn', 'Year-round'])
                altitude = np.random.randint(500, 2000)
                
            elif any(word in name.lower() for word in ['market', 'bazaar', 'shopping']):
                category = 'Market/Shopping'
                difficulty = 'Easy'
                duration = 0.5
                cost = np.random.randint(20, 100)
                best_season = 'Year-round'
                altitude = np.random.randint(500, 2000)
                
            else:
                category = np.random.choice(['Trekking', 'Cultural Heritage', 'Nature & Wildlife', 
                                            'Religious Site', 'Adventure Sports', 'Hill Station', 
                                            'Market/Shopping', 'Lake', 'Historical Site'])
                difficulty = np.random.choice(difficulties)
                duration = np.random.randint(1, 14)
                cost = np.random.randint(50, 1000)
                best_season = np.random.choice(['Spring', 'Summer', 'Autumn', 'Winter', 'Year-round'])
                altitude = np.random.randint(500, 2000)
            
            # Assign region based on name (fallback)
            if 'everest' in name.lower() or 'khumbu' in name.lower() or 'namche' in name.lower() or 'tengboche' in name.lower() or 'lukla' in name.lower():
                region = 'Everest Region'
            elif 'annapurna' in name.lower() or 'poon hill' in name.lower() or 'ghandruk' in name.lower():
                region = 'Annapurna Region'
            elif 'pokhara' in name.lower() or 'sarangkot' in name.lower() or 'world peace' in name.lower() or 'mahendra' in name.lower() or 'tal barahi' in name.lower():
                region = 'Pokhara Region'
            elif 'kathmandu' in name.lower() or 'patan' in name.lower() or 'bhaktapur' in name.lower() or 'swayambhunath' in name.lower() or 'boudhanath' in name.lower() or 'pashupatinath' in name.lower() or 'garden of dreams' in name.lower() or 'thamel' in name.lower() or 'kopan' in name.lower() or 'nagarkot' in name.lower() or 'dhulikhel' in name.lower():
                region = 'Kathmandu Valley'
            elif 'langtang' in name.lower() or 'gosaikunda' in name.lower():
                region = 'Langtang Region'
            elif 'mustang' in name.lower() or 'muktinath' in name.lower() or 'kagbeni' in name.lower() or 'jomsom' in name.lower():
                region = 'Mustang Region'
            elif 'manaslu' in name.lower():
                region = 'Manaslu Region'
            elif 'chitwan' in name.lower():
                region = 'Chitwan'
            elif 'lumbini' in name.lower() or 'janakpur' in name.lower() or 'koshi tappu' in name.lower():
                region = 'Lumbini'
            elif 'rara' in name.lower() or 'bardiya' in name.lower():
                region = 'Far West Nepal'
            else:
                region = np.random.choice(['Kathmandu Valley', 'Pokhara Region', 'Everest Region', 
                                         'Annapurna Region', 'Chitwan', 'Lumbini', 'Far West Nepal',
                                         'Langtang Region', 'Manaslu Region', 'Mustang Region'])
        
        # Beta distribution with parameters (8,2) gives us ratings mostly between 3.5-5.0
        rating = np.random.beta(8, 2) * 5
        rating = round(rating, 1)
        rating = max(3.0, min(5.0, rating))
        
        # Number of reviews (more popular places have more reviews)
        # Exponential distribution gives realistic distribution (few very popular, many moderately popular)
        num_reviews = int(np.random.exponential(400) + 50)
        num_reviews = min(num_reviews, 5000)  # Cap at 5000 reviews
        
        # Create description
        description = f"A {difficulty.lower()} {category.lower()} experience in {region}."
        
        # Build attraction dictionary
        attraction = {
            'attraction_id': i,
            'name': name,
            'category': category,
            'region': region,
            'rating': rating,
            'num_reviews': num_reviews,
            'avg_cost_usd': cost,
            'duration_days': duration,
            'difficulty': difficulty,
            'best_season': best_season,
            'altitude_meters': altitude,
            'description': description
        }
        
        attractions.append(attraction)
    
    df = pd.DataFrame(attractions)
    
    print(f"... Created {len(df)} attractions")
    return df


def generate_user_ratings(attractions_df, num_users=200, avg_ratings_per_user=14):
    
    print(f"👥 Generating ratings from {num_users} users...")
    
    ratings = []
    attraction_ids = attractions_df['attraction_id'].tolist()
    
    for user_id in range(num_users):
        # Each user rates different number of attractions (some rate more, some less)
        num_ratings = max(3, int(np.random.normal(avg_ratings_per_user, 5)))
        num_ratings = min(num_ratings, len(attraction_ids))  # Can't rate more than total attractions
        
        # Randomly select which attractions this user visited
        visited_attractions = np.random.choice(
            attraction_ids,
            size=num_ratings,
            replace=False  # Can't visit same attraction twice
        )
        
        for attraction_id in visited_attractions:
            # Get the attraction's average rating
            attr_avg_rating = attractions_df[
                attractions_df['attraction_id'] == attraction_id
            ]['rating'].values[0]
            
            # User's rating is close to average but with personal variation
            # Normal distribution around attraction's rating
            user_rating = attr_avg_rating + np.random.normal(0, 0.7)
            
            # Keep rating between 1 and 5
            user_rating = max(1, min(5, user_rating))
            user_rating = round(user_rating)  # Round to integer (1,2,3,4,5)
            
            # Random date in past year
            days_ago = np.random.randint(1, 365)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            ratings.append({
                'user_id': user_id,
                'attraction_id': attraction_id,
                'rating': user_rating,
                'timestamp': timestamp
            })
    
    ratings_df = pd.DataFrame(ratings)
    
    print(f"... Created {len(ratings_df)} ratings")
    print(f" ... Average: {len(ratings_df)/num_users:.1f} ratings per user")
    
    return ratings_df


def generate_user_preferences(num_users=200):
    
    print(f"... Generating {num_users} user profiles...")
    
    categories = [
        'Trekking', 'Cultural Heritage', 'Nature & Wildlife', 
        'Religious Site', 'Adventure Sports'
    ]
    
    users = []
    
    for user_id in range(num_users):
        user = {
            'user_id': user_id,
            'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-60', '60+']),
            'budget_level': np.random.choice(['Budget', 'Mid-range', 'Luxury']),
            'fitness_level': np.random.choice(['Low', 'Medium', 'High']),
            'preferred_category': np.random.choice(categories),
            'travel_style': np.random.choice(['Solo', 'Couple', 'Family', 'Group']),
            'origin_country': np.random.choice(['USA', 'UK', 'India', 'China', 'Australia', 'Germany', 'France', 'Japan'])
        }
        users.append(user)
    
    users_df = pd.DataFrame(users)
    
    print(f"Success! Created {len(users_df)} user profiles")
    
    return users_df


def main():
    
    print("\n" + "="*60)
    print("="*60 + "\n")
    
    # Generate all three datasets
    attractions_df = generate_attractions_data(num_attractions=50)
    ratings_df = generate_user_ratings(attractions_df, num_users=200)
    users_df = generate_user_preferences(num_users=200)
    
    print("\n" + "="*60)
    # print(" Saving data to CSV files...")
    print("="*60 + "\n")
    
    # Save to CSV files in data/processed/ folder
    attractions_df.to_csv('data/processed/attractions.csv', index=False)
    ratings_df.to_csv('data/processed/user_ratings.csv', index=False)
    users_df.to_csv('data/processed/users.csv', index=False)
    
    # print(" Saved: data/processed/attractions.csv")
    # print(" Saved: data/processed/user_ratings.csv")
    # print(" Saved: data/processed/users.csv")
    
    # Display summary statistics
    print("\n" + "="*60)
    print("Dataset Summary")
    print("="*60 + "\n")
    
    print(f"Total Attractions: {len(attractions_df)}")
    print(f"Total Ratings: {len(ratings_df)}")
    print(f"Total Users: {len(users_df)}")
    print(f"\nAverage Rating: {attractions_df['rating'].mean():.2f}/5.0")
    print(f"Most Expensive: ${attractions_df['avg_cost_usd'].max()}")
    print(f"Cheapest: ${attractions_df['avg_cost_usd'].min()}")
    
    print(f"\nCategories ({attractions_df['category'].nunique()}):")
    for cat, count in attractions_df['category'].value_counts().items():
        print(f"  • {cat}: {count}")
    
    print(f"\nRegions ({attractions_df['region'].nunique()}):")
    for region, count in attractions_df['region'].value_counts().head(5).items():
        print(f"  • {region}: {count}")
    
    print("\n" + "="*60)
    # print("Success!!!! Data generation complete!")
    print("="*60 + "\n")
    
    # Show sample attractions
    print("Sample Attractions:")
    print("-" * 60)
    sample = attractions_df[['name', 'category', 'rating', 'avg_cost_usd', 'difficulty']].head(10)
    print(sample.to_string(index=False))
    

if __name__ == '__main__':
    main()