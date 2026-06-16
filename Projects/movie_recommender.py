import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        # Preprocessing: Merge relevant columns into a single "tags" feature
        self.df['overview'] = self.df['overview'].fillna('')
        self.df['tags'] = self.df['genres'] + " " + self.df['overview']
        self.df['tags'] = self.df['tags'].apply(lambda x: x.lower())
        
        # Vectorization: Convert text tags to numeric frequency vectors
        self.cv = CountVectorizer(max_features=5000, stop_words='english')
        self.vector_matrix = self.cv.fit_transform(self.df['tags']).toarray()
        
        # Similarity Matrix: Compute cosine similarity between all vectors
        self.similarity = cosine_similarity(self.vector_matrix)

    def get_recommendations(self, movie_title: str, top_n: int = 5):
        """Finds top N similar movies based on content vector distance."""
        movie_title = movie_title.lower()
        
        # Search for index
        indices = self.df[self.df['title'].str.lower() == movie_title].index
        if len(indices) == 0:
            return f"Error: Movie '{movie_title}' not found in database."
        
        idx = indices[0]
        
        # Get similarity scores, sort descending, skip the first (itself)
        distances = self.similarity[idx]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
        
        results = []
        for i in movies_list:
            results.append(self.df.iloc[i[0]].title)
        return results

# --- Execution ---
if __name__ == "__main__":
    try:
        recommender = MovieRecommender('tmdb_5000_movies.csv')
        
        user_movie = input("Enter a movie name you liked: ")
        print(f"\nAnalyzing patterns for '{user_movie}'...")
        
        recommendations = recommender.get_recommendations(user_movie)
        
        if isinstance(recommendations, list):
            print(f"\nBecause you watched '{user_movie}', you might also like:")
            for i, movie in enumerate(recommendations, 1):
                print(f"{i}. {movie}")
        else:
            print(recommendations)
            
    except FileNotFoundError:
        print("Critical Error: Ensure 'tmdb_5000_movies.csv' is in the project directory.")