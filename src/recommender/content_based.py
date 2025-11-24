"""
Content-Based Recommendation System
Recommends attractions based on feature similarity.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack, csr_matrix


class ContentBasedRecommender:
    """
    Content-based filtering recommender system.
    Recommends attractions similar to ones the user has shown interest in.
    """
    
    def __init__(self):
        self.attractions_df = None
        self.similarity_matrix = None
        self.feature_matrix = None
        
    def fit(self, attractions_df):
        """
        Train the recommender on attraction features.
        
        Parameters:
            attractions_df: DataFrame containing attraction information
        """
        self.attractions_df = attractions_df.copy()
        
        # Combine text features
        self.attractions_df['text_features'] = (
            self.attractions_df['category'] + ' ' +
            self.attractions_df['region'] + ' ' +
            self.attractions_df['difficulty'] + ' ' +
            self.attractions_df['best_season']
        )
        
        # Create TF-IDF vectors
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.attractions_df['text_features'])
        
        # Normalize numerical features
        scaler = MinMaxScaler()
        numerical_features = self.attractions_df[[
            'rating', 'avg_cost_usd', 'duration_days'
        ]].values
        numerical_normalized = scaler.fit_transform(numerical_features)
        
        # Combine text and numerical features
        self.feature_matrix = hstack([
            tfidf_matrix,
            csr_matrix(numerical_normalized)
        ])
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(self.feature_matrix)
        
        return self
    
    def recommend(self, attraction_id, top_n=5, min_similarity=0.1):
        """
        Get similar attractions based on content features.
        
        Parameters:
            attraction_id: ID of the attraction
            top_n: Number of recommendations to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            DataFrame with recommended attractions
        """
        if attraction_id >= len(self.attractions_df):
            raise ValueError(f"Invalid attraction_id: {attraction_id}")
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[attraction_id]))
        
        # Sort by similarity, excluding the item itself
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]
        
        # Filter by minimum similarity
        sim_scores = [(i, score) for i, score in sim_scores if score >= min_similarity]
        
        # Get top N
        sim_scores = sim_scores[:top_n]
        
        # Extract indices and scores
        attraction_indices = [i for i, _ in sim_scores]
        similarity_scores = [score for _, score in sim_scores]
        
        # Build recommendations dataframe
        recommendations = self.attractions_df.iloc[attraction_indices].copy()
        recommendations['similarity_score'] = similarity_scores
        
        return recommendations[[
            'attraction_id', 'name', 'category', 'region', 
            'rating', 'avg_cost_usd', 'similarity_score'
        ]]
    
    def recommend_by_preferences(self, preferred_category=None, 
                                 max_cost=None, difficulty=None, top_n=10):
        """
        Filter and recommend attractions based on user preferences.
        
        Parameters:
            preferred_category: Category filter
            max_cost: Maximum budget in USD
            difficulty: Difficulty level filter
            top_n: Number of recommendations
            
        Returns:
            DataFrame with filtered attractions
        """
        filtered = self.attractions_df.copy()
        
        if preferred_category:
            filtered = filtered[filtered['category'] == preferred_category]
        
        if max_cost:
            filtered = filtered[filtered['avg_cost_usd'] <= max_cost]
        
        if difficulty:
            filtered = filtered[filtered['difficulty'] == difficulty]
        
        # Calculate popularity score
        filtered['popularity_score'] = (
            filtered['rating'] * 0.7 + 
            (filtered['num_reviews'] / filtered['num_reviews'].max()) * 5 * 0.3
        )
        
        recommendations = filtered.nlargest(top_n, 'popularity_score')
        
        return recommendations[[
            'attraction_id', 'name', 'category', 'region', 
            'rating', 'avg_cost_usd', 'duration_days', 'difficulty'
        ]]


if __name__ == '__main__':
    # Load data
    attractions = pd.read_csv('data/processed/attractions.csv')
    
    # Initialize and train recommender
    print("Training Content-Based Recommender...")
    print()
    recommender = ContentBasedRecommender()
    recommender.fit(attractions)
    
    # Test 1: Find similar attractions
    print("-" * 70)
    print("Test 1: Similar Attractions")
    print("-" * 70)
    original = attractions.iloc[0]
    print(f"Original: {original['name']}")
    print(f"Category: {original['category']}, Region: {original['region']}")
    print(f"Rating: {original['rating']}/5.0, Cost: ${original['avg_cost_usd']}")
    print()
    
    print("Similar attractions:")
    recommendations = recommender.recommend(attraction_id=0, top_n=5)
    print(recommendations.to_string(index=False))
    print()
    
    # Test 2: Preference-based recommendations
    print("-" * 70)
    print("Test 2: Trekking Recommendations (Budget under $1000)")
    print("-" * 70)
    prefs = recommender.recommend_by_preferences(
        preferred_category='Trekking',
        max_cost=1000,
        top_n=5
    )
    print(prefs.to_string(index=False))
