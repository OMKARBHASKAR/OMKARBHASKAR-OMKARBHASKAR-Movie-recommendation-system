import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class RecommendationEngine:
    def __init__(self, csv_path='movies_with_posters.csv'):
        # Manual parsing to handle unquoted commas in description
        print("DEBUG: Loading movies manually with split fix...")
        data = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Skip header
                for line in lines[1:]:
                    if not line.strip(): continue
                    # Split on commas: Title, Genres, Description, Poster_URL, TMDB_ID
                    parts = line.strip().split(',', 4)
                    if len(parts) >= 4:
                        # Clean up the fields
                        clean_parts = [p.strip().strip('"') for p in parts[:4]]
                        data.append(clean_parts)
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        self.df = pd.DataFrame(data, columns=['title', 'genres', 'description', 'poster_url'])
        print(f"DEBUG: Loaded {len(self.df)} movies.")
        if not self.df.empty:
            print(f"DEBUG: Sample titles: {self.df['title'].head().tolist()}")
        
        # Create a soup of relevant metadata: genres + description
        self.df['content'] = self.df['genres'] + " " + self.df['description']
        
        # Fill NaN with empty string
        self.df['content'] = self.df['content'].fillna('')
        
        # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # Construct the required TF-IDF matrix by fitting and transforming the data
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['content'])
        
        # Compute the cosine similarity matrix
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        
        # Construct a reverse map of indices and movie titles
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()



    def get_movie_details(self, title):
        """Get movie details from the CSV dataset"""
        try:
            # Look up the movie in our dataframe
            movie_row = self.df[self.df['title'] == title]
            
            if movie_row.empty:
                # Try case-insensitive match
                movie_row = self.df[self.df['title'].str.lower() == title.lower()]
            
            if not movie_row.empty:
                return {
                    'title': movie_row.iloc[0]['title'],
                    'poster_url': movie_row.iloc[0]['poster_url'],
                    'genres': movie_row.iloc[0]['genres'],
                    'description': movie_row.iloc[0]['description']
                }
            return None
        except Exception as e:
            print(f"Error fetching details for {title}: {e}")
            return None

    def get_recommendations(self, title, num_recommendations=5):
        # Check if title exists (case-insensitive search attempt)
        if title not in self.indices:
            # Try to find a partial match
            titles = self.df['title'].tolist()
            matches = [t for t in titles if title.lower() in t.lower()]
            if not matches:
                return []
            title = matches[0] # Use the first match
        
        idx = self.indices[title]
        
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:num_recommendations+1]
        
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return the top most similar movies
        return self.df['title'].iloc[movie_indices].tolist()

if __name__ == "__main__":
    # Test
    recommender = RecommendationEngine()
    print("Recommendations for 'The Dark Knight':")
    print(recommender.get_recommendations('The Dark Knight'))
