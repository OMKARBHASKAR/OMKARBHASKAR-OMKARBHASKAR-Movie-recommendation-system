import streamlit as st
import pandas as pd
from recommendation_engine import RecommendationEngine

# Page Config
st.set_page_config(
    page_title="CineMate - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Wow" factor
st.markdown("""
<style>
    /* Main Background - Darker Theme */
    .stApp {
        background: linear-gradient(to bottom right, #0a0e1a, #0f172a);
        color: #f8fafc;
    }
    
    /* Input Field */
    .stTextInput > div > div > input {
        background-color: #334155;
        color: #f8fafc;
        border: 2px solid #475569;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    
    /* Headers - Bigger and Bolder */
    h1 {
        background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        font-weight: 900 !important;
    }
    
    /* Input Label - White and Bigger */
    .stTextInput > label {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* Cards */
    .movie-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
        text-align: center;
        height: 100%;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        background-color: rgba(255, 255, 255, 0.1);
        border-color: #38bdf8;
    }
    .movie-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 10px;
        color: #e2e8f0;
    }
    .movie-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Recommendation Engine
@st.cache_resource
def load_engine():
    return RecommendationEngine()

recommender = load_engine()

# Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("Movie Recommender System")
    st.markdown("### Discover your next favorite movie")
    
    # Get all movie titles from the dataset
    all_movies = recommender.df['title'].tolist()
    
    # Selectbox with all movies
    movie_name = st.selectbox(
        "Select a movie",
        options=[""] + all_movies,  # Empty option first
        index=0,
        help="Choose a movie from the dropdown to get recommendations"
    )
    
    if st.button("Get Recommendations"):
        if movie_name:
            with st.spinner("Finding matches..."):
                recommendations = recommender.get_recommendations(movie_name)
                
            if recommendations:
                st.markdown("---")
                
                
                # Display results in columns - 4 columns for larger images
                cols = st.columns(4)
                for idx, rec_title in enumerate(recommendations[:4]):  # Show top 4 for larger display
                    with cols[idx]:
                        # Fetch details
                        details = recommender.get_movie_details(rec_title)
                        
                        poster_url = details.get('poster_url') if details else "https://via.placeholder.com/300x450?text=No+Poster"
                        display_title = details.get('title', rec_title) if details else rec_title
                        
                        st.image(poster_url, use_container_width=True)
                        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 1.1rem; margin-top: 10px;'>{display_title}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a movie name first.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #94a3b8;'>Built with ❤️ using Streamlit & Python</div>", unsafe_allow_html=True)
