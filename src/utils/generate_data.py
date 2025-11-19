import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)


def generate_attractions_data(num_attractions=50):

    print(f"  Generating {num_attractions} attractions...")
    
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
    
    # Possible categories
    categories = [
        'Trekking', 
        'Cultural Heritage', 
        'Nature & Wildlife', 
        'Religious Site', 
        'Adventure Sports', 
        'Hill Station', 
        'Market/Shopping',
        'Lake',
        'Historical Site'
    ]
    
    regions = [
        'Kathmandu Valley',
        'Pokhara Region',
        'Everest Region',
        'Annapurna Region',
        'Chitwan',
        'Lumbini',
        'Far West Nepal',
        'Langtang Region',
        'Manaslu Region',
        'Mustang Region'
    ]
    
    
    difficulties = ['Easy', 'Easy-Moderate', 'Moderate', 'Moderate-Hard', 'Hard', 'Extreme']
    
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter', 'Year-round']
    
    attractions = []
    
    for i, name in enumerate(selected_attractions):
        
        if any(word in name.lower() for word in ['trek', 'circuit', 'base camp', 'hike']):
            category = 'Trekking'
            difficulty = np.random.choice(['Moderate', 'Moderate-Hard', 'Hard', 'Extreme'])
            duration = np.random.randint(7, 21)
            cost = np.random.randint(500, 1500)
            best_season = np.random.choice(['Spring', 'Autumn'])
            
        elif any(word in name.lower() for word in ['temple', 'stupa', 'monastery', 'lumbini']):
            category = 'Religious Site'
            difficulty = 'Easy'
            duration = 1
            cost = np.random.randint(10, 50)
            best_season = 'Year-round'
            
        elif any(word in name.lower() for word in ['lake', 'river', 'waterfall']):
            category = 'Nature & Wildlife'
            difficulty = np.random.choice(['Easy', 'Moderate', 'Hard'])
            duration = np.random.randint(1, 7)
            cost = np.random.randint(50, 400)
            best_season = np.random.choice(['Spring', 'Summer', 'Autumn'])
            
        elif any(word in name.lower() for word in ['durbar square', 'palace', 'historic']):
            category = 'Cultural Heritage'
            difficulty = 'Easy'
            duration = 1
            cost = np.random.randint(15, 40)
            best_season = 'Year-round'
            
        elif any(word in name.lower() for word in ['paragliding', 'bungee', 'rafting']):
            category = 'Adventure Sports'
            difficulty = np.random.choice(['Moderate', 'Hard'])
            duration = 1
            cost = np.random.randint(80, 200)
            best_season = np.random.choice(['Spring', 'Autumn', 'Year-round'])
            
        elif any(word in name.lower() for word in ['market', 'bazaar', 'shopping']):
            category = 'Market/Shopping'
            difficulty = 'Easy'
            duration = 0.5
            cost = np.random.randint(20, 100)
            best_season = 'Year-round'
            
        else:
            category = np.random.choice(categories)
            difficulty = np.random.choice(difficulties)
            duration = np.random.randint(1, 14)
            cost = np.random.randint(50, 1000)
            best_season = np.random.choice(seasons)
        
        
        # Beta distribution with parameters (8,2) gives us ratings mostly between 3.5-5.0
        rating = np.random.beta(8, 2) * 5
        rating = round(rating, 1)
        rating = max(3.0, min(5.0, rating))
        
        # Number of reviews (more popular places have more reviews)
        # Exponential distribution gives realistic distribution (few very popular, many moderately popular)
        num_reviews = int(np.random.exponential(400) + 50)
        num_reviews = min(num_reviews, 5000)  # Cap at 5000 reviews
        
        # Altitude (meters above sea level)
        if 'everest' in name.lower():
            altitude = np.random.randint(4000, 5500)
        elif category == 'Trekking':
            altitude = np.random.randint(2000, 4500)
        else:
            altitude = np.random.randint(500, 2000)
        
        # Assign region based on name
        if 'everest' in name.lower() or 'khumbu' in name.lower():
            region = 'Everest Region'
        elif 'annapurna' in name.lower() or 'pokhara' in name.lower():
            region = 'Annapurna Region'
        elif 'kathmandu' in name.lower() or 'patan' in name.lower() or 'bhaktapur' in name.lower():
            region = 'Kathmandu Valley'
        elif 'langtang' in name.lower():
            region = 'Langtang Region'
        elif 'mustang' in name.lower():
            region = 'Mustang Region'
        elif 'chitwan' in name.lower():
            region = 'Chitwan'
        else:
            region = np.random.choice(regions)
        
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
    
    # Convert list of dictionaries to DataFrame (table)
    df = pd.DataFrame(attractions)
    
    print(f"✅ Created {len(df)} attractions")
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
    
    print(f"✅ Created {len(ratings_df)} ratings")
    print(f"   Average: {len(ratings_df)/num_users:.1f} ratings per user")
    
    return ratings_df


def generate_user_preferences(num_users=200):
    """
    Generate user preference profiles.
    
    This gives each user characteristics like age, budget, fitness level.
    Useful for future personalized recommendations.
    
    Parameters:
    -----------
    num_users : int
        Number of user profiles to create
    
    Returns:
    --------
    DataFrame
        User profiles with preferences
    """
    
    print(f"📋 Generating {num_users} user profiles...")
    
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
    
    print(f"✅ Created {len(users_df)} user profiles")
    
    return users_df


def main():
    """
    Main function - runs when script is executed.
    Generates all data and saves to CSV files.
    """
    
    print("\n" + "="*60)
    print("🇳🇵  Nepal Tourism Dataset Generator")
    print("="*60 + "\n")
    
    # Generate all three datasets
    attractions_df = generate_attractions_data(num_attractions=50)
    ratings_df = generate_user_ratings(attractions_df, num_users=200)
    users_df = generate_user_preferences(num_users=200)
    
    print("\n" + "="*60)
    print("💾 Saving data to CSV files...")
    print("="*60 + "\n")
    
    # Save to CSV files in data/processed/ folder
    attractions_df.to_csv('data/processed/attractions.csv', index=False)
    ratings_df.to_csv('data/processed/user_ratings.csv', index=False)
    users_df.to_csv('data/processed/users.csv', index=False)
    
    print("✅ Saved: data/processed/attractions.csv")
    print("✅ Saved: data/processed/user_ratings.csv")
    print("✅ Saved: data/processed/users.csv")
    
    # Display summary statistics
    print("\n" + "="*60)
    print("📊 Dataset Summary")
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
    print("🎉 Data generation complete!")
    print("="*60 + "\n")
    
    # Show sample attractions
    print("Sample Attractions:")
    print("-" * 60)
    sample = attractions_df[['name', 'category', 'rating', 'avg_cost_usd', 'difficulty']].head(10)
    print(sample.to_string(index=False))
    
    print("\n✨ Next steps:")
    print("  1. Explore the data: jupyter notebook notebooks/01_data_exploration.ipynb")
    print("  2. Build recommender: Create src/recommender/content_based.py")
    print("  3. Test it: python demo.py")


# This runs when you execute: python generate_data.py
if __name__ == '__main__':
    main()