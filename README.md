# 🎬 Movie Recommender System

A content-based movie recommendation system built with Python and Streamlit, featuring movie posters from TMDB.

## Features

- 🎯 Content-based recommendation using TF-IDF vectorization
- 🖼️ Movie posters from TMDB
- 🎨 Modern dark-themed UI
- ⚡ Fast recommendations
- 📊 Dataset of 40 popular movies

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd anitgravity-ff
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

Or:
```bash
py -m streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## How It Works

1. Enter a movie name from the dataset
2. The system uses TF-IDF vectorization on movie genres and descriptions
3. Cosine similarity finds the most similar movies
4. Top 3 recommendations are displayed with posters

## Dataset

The `movies_with_posters.csv` contains:
- Movie titles
- Genres
- Descriptions
- TMDB poster URLs
- TMDB IDs

## Technologies

- **Python 3.x**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - TF-IDF vectorization and similarity calculation

## Project Structure

```
.
├── streamlit_app.py           # Main Streamlit application
├── recommendation_engine.py   # Recommendation logic
├── movies_with_posters.csv    # Movie dataset with poster URLs
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## License

MIT License
