import streamlit as st
from streamlit_card import card
from streamlit_option_menu import option_menu
import os
import zipfile
import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from movie import *
import requests
from concurrent.futures import ThreadPoolExecutor


def search_movies(query, data_items):
    """Search for movies in the dataset based on query"""
    # Convert query and movie names to lowercase for case-insensitive search
    query = query.lower()
    # Filter movies where movie name contains the search query
    matches = data_items[data_items['movie_name'].str.lower().str.contains(query, na=False)]
    return matches

def fetch_movie_details(movie_name):
    """Fetch movie details from TMDB API"""
    api_key = "8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    base_url = "https://api.themoviedb.org/3"
    
    search_url = f"{base_url}/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_name
    }
    
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            movie = data["results"][0]
            return {
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else "https://via.placeholder.com/500x750?text=No+Poster+Available",
                "overview": movie['overview'],
                "release_date": movie['release_date'],
                "rating": movie['vote_average'],
                "id": movie['id']
            }
    except:
        pass
    
    return {
        "poster_path": "https://via.placeholder.com/500x750?text=No+Poster+Available",
        "overview": "No overview available",
        "release_date": "Unknown",
        "rating": "N/A",
        "id": None
    }


def fetch_movie_poster(movie_name):
    api_key = "8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    base_url = "https://api.themoviedb.org/3"

    search_url = f"{base_url}/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_name
    }
    
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            poster_path = data["results"][0]["poster_path"]
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    
    # Return a placeholder if no poster is found
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def display_movie_cards(movies, title):
    """Display movie recommendations as cards"""
    st.subheader(title)
    
    # Create rows of 4 movies each
    cols = st.columns(4)
    for idx, movie in enumerate(movies):
        col_idx = idx % 4
        with cols[col_idx]:
            # Fetch poster URL for the movie
            poster_url = fetch_movie_poster(movie)
            
            # Create card using HTML/CSS
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 10px 0;
                    text-align: center;
                    height: 400px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                ">
                    <img src="{poster_url}" 
                        style="
                            width: 100%;
                            height: 300px;
                            object-fit: cover;
                            border-radius: 4px;
                        "
                    >
                    <h4 style="
                        margin: 10px 0;
                        font-size: 1rem;
                        height: 50px;
                        overflow: hidden;
                    ">{movie}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Start a new row after every 4 movies
        if col_idx == 3:
            cols = st.columns(4)


# Function to display home page content

def display_home_page():
    st.title("Welcome to ShowShuffle")

    st.write("""
        Welcome to my Movie Recommendation System! This platform is designed to help you discover new movies tailored to your tastes.
        Our advanced recommendation algorithms analyze various aspects of movies to suggest the best matches for you.
    """)

    st.header("How It Works")
    st.write("""
        My recommendation system uses a combination of collaborative filtering and content-based filtering techniques to provide personalized movie recommendations. Here’s a brief overview of the process:

        1. **Data Collection**: I gathered data from various sources including movie ratings, genres, cast, and user preferences.
        2. **Model Training**: The machine learning models analyze the data to understand patterns and relationships between different movies and users' preferences.
        3. **Recommendation Generation**: Based on the trained models, it generates a list of recommended movies for each user.

        This approach ensures that you receive recommendations that are not only popular but also align with your individual tastes.
    """)

    st.header("Features")
    st.write("""
        - **Personalized Recommendations**: Get suggestions based on your viewing history and preferences.
        - **Wide Variety**: Discover movies from different genres, directors, and time periods.
        - **User-Friendly Interface**: Easily navigate and find new movies to watch.
        - **Regular Updates**: The database is constantly updated with new movies and ratings to ensure up-to-date recommendations.

        I aim to enhance your movie-watching experience by making it easier for you to find movies you’ll love.
    """)

    st.header("Benefits")
    st.write("""
        - **Save Time**: No more endless scrolling through streaming services. Our system quickly finds movies you'll enjoy.
        - **Discover Hidden Gems**: Uncover lesser-known movies that match your taste.
        - **Enhanced Viewing Experience**: Personalized suggestions mean you'll always have something interesting to watch.
        - **Stay Updated**: Be in the know about the latest movies and trending picks.

        With our movie recommendation system, your next favorite movie is just a click away!
    """)

    st.header("Get Started")
    st.write("""
        Stay tuned for the launch of our interactive movie recommendation feature. Soon, you’ll be able to input your preferences and get personalized movie suggestions right here!

        In the meantime, feel free to explore our website and learn more about how our recommendation system can enhance your movie-watching experience.
    """)
    st.write("---")
    st.write("### Contact Me")
    st.write("""
        If you have any questions or feedback, please don't hesitate to reach out to me at tejaswimahadev9@gmail.com.
    """)
    st.write("---")

# Function to display category page content
def action_page():
    st.title("WHAT TO WATCH")
    st.header("Top picks")

def display_category_page():
    st.title("Categories")
    
    # Create expandable sections for each genre
    with st.expander("ACTION", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Top Gun: Maverick",
                text="After thirty years, Maverick is still pushing the envelope as a top naval aviator.",
                image="https://m.media-amazon.com/images/M/MV5BZWYzOGEwNTgtNWU3NS00ZTQ0LWJkODUtMmVhMjIwMjA1ZmQwXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="John Wick",
                text="An ex-hitman comes out of retirement to track down the gangsters that killed his dog.",
                image="https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )

    with st.expander("SCIENCE FICTION", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Inception",
                text="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                image="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="Blade Runner 2049",
                text="A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.",
                image="https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    with st.expander("HORROR", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="The Conjuring",
                text="------------------------------------------",
                image="https://image.tmdb.org/t/p/original/ue0dKuJUhIK4aLr4YcZcNa23saL.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="The Shining",
                text="--------------------------------------------",
                image="https://i.pinimg.com/originals/9b/e0/b9/9be0b9b18147860cdf09d543009cb1d7.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    with st.expander("ANIMATION", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Spiderman - Across the Spider-Verse",
                text="------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.V0ustTI4Xr26oBuCCEV7GAHaK8&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="Your Name",
                text="--------------------------------------------",
                image="https://m.media-amazon.com/images/M/MV5BNTQyMDQwYTUtMDdlMC00YTczLTk2NDktZDRjZDEyZjJmNGQzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    with st.expander("ROMANCE", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="The Notebook",
                text="------------------------------------------",
                image="https://image.tmdb.org/t/p/original/wbvboxr6xmdSbMEBKzXVWgAwJ1Q.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="Pride and Prejudice",
                text="--------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.NGVYslLQv9LQr0iBtNpIYwHaJ4&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    
    with st.expander("THRILLER", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Gone Girl",
                text="------------------------------------------",
                image="https://upload.wikimedia.org/wikipedia/en/7/7e/Gone_Girl_%28Flynn_novel%29.jpg",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="Se7en",
                text="--------------------------------------------",
                image="https://tse1.mm.bing.net/th?id=OIP.8oB6jMVpgxBpyXwv6iz-4wHaKf&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    
    with st.expander("COMEDY", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="The Grand Budapest Hotel",
                text="------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.eqw9zTSb2p2SKwaElnbQNQHaLH&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="Superbad",
                text="--------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.y1WWTnkVfWsrCyXUyoSL-AHaKj&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
    
    with st.expander("DOCUMENTARY", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Free Solo",
                text="------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.pZqKMB7LBkDXugRNvl22HgHaJ4&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )
        
        with col2:
            card(
                title="March of the Penguins",
                text="--------------------------------------------",
                image="https://tse4.mm.bing.net/th?id=OIP.QE94iI6Dn4s_hbHEe5rV9AHaLH&pid=Api&P=0&h=180",
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px",
                        "border-radius": "10px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                    "text": {
                        "font-family": "serif",
                        "text-align": "center",
                    }
                }
            )

  
# Main function to control page navigation
def load_data():
    # Extract the zip file if it hasn't been extracted yet
    zip_file_path = './archive.zip'
    extract_to_path = './archive'
    
    if not os.path.exists(extract_to_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            zf.extractall(extract_to_path)
    
    data_ = os.path.join(extract_to_path, 'ml-100k')

    # Load data
    data_users = pd.read_csv(os.path.join(data_, 'u.user'), sep='|', names=['user_id', 'age', 'gender', 'occupation', 'zip_code'], encoding='latin-1').set_index('user_id')
    cols = [
        'movie_id', 'movie_name', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure', 'animation', 'children',
        'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film-noir', 'horror', 'musical', 'mystery', 'romance', 'sci-fi', 'thriller', 'war',
        'western'
    ]
    data_items = pd.read_csv(os.path.join(data_, 'u.item'), sep='|', encoding='latin-1', names=cols).set_index('movie_id')
    data_data = pd.read_csv(os.path.join(data_, 'u.data'), names=['user_id', 'movie_id', 'rating', 'time_stamp'], sep='\t', encoding='latin-1').set_index('user_id')

    return data_users, data_items, data_data

data_users, data_items, data_data = load_data()

def recom_movies(n):
    movie_sort = movie_mean.sort_values(ascending=False)[:n]
    recom_movies = data_items.loc[movie_sort.index]
    recommendations = recom_movies['movie_name']
    return recommendations

### Personalized Recommendations
data_data_coh = data_data.drop(columns=['time_stamp']).reset_index()
data_items_coh = data_items[['movie_name']].reset_index()
rating_matrix = data_data_coh.pivot(index='user_id', columns='movie_id', values='rating')

user_similarity = cosine_similarity(rating_matrix.fillna(0))
user_similarity_df = pd.DataFrame(user_similarity, index=rating_matrix.index, columns=rating_matrix.index)
### Popularity based recommendation
movie_mean = data_data.groupby(['movie_id'])['rating'].mean()
def cf_knn(user_id, movie_id):
    if movie_id in rating_matrix:
        sim_scores = user_similarity_df[user_id].copy()
        movie_ratings = rating_matrix[movie_id].copy()
        none_rating_index = movie_ratings[movie_ratings.isnull()].index
        movie_ratings = movie_ratings.drop(none_rating_index)
        sim_scores = sim_scores.drop(none_rating_index)
        mean_rating = np.dot(sim_scores, movie_ratings) / sim_scores.sum()
        return mean_rating
    return 0

def recom_movies_cf(user_id, n):
    user_movie = rating_matrix.loc[user_id].copy()
    for movie in rating_matrix:
        if pd.notnull(user_movie.loc[movie]):
            user_movie.loc[movie] = 0
        else:
            user_movie.loc[movie] = cf_knn(user_id, movie)
    movie_sort = user_movie.sort_values(ascending=False)[:n]
    recom_movies = data_items_coh.loc[movie_sort.index]
    recommendations = recom_movies['movie_name']
    return recommendations
def main():
        st.sidebar.markdown(
        """
        <h1 style='font-size: 2em;'>
            <img src="https://img.icons8.com/?size=100&id=100010&format=png&color=000000" alt="Swift Icon" style="vertical-align: middle;">ShowShuffle
        </h1>
        """,
        unsafe_allow_html=True
    )
        st.sidebar.header("NAVIGATION")
        with st.sidebar.expander("Menu",expanded=True):

            page = option_menu(menu_title="Navigation",options=["Home","Categories","Movies"],icons=["house","list","cast"],menu_icon="star",default_index=0)

        if page == "Home":
            display_home_page()
        elif page == "Categories":
            display_category_page()
        elif page == "Movies":
            st.title("Movies")
    
    # Popularity-based Recommendations
            st.write("### Popularity-based Recommendations")
            num_recommendations = st.slider("Number of recommendations", 1, 20, 8)
    
            if st.button("Get Popular Movies"):
                popular_movies = recom_movies(num_recommendations)
                display_movie_cards(popular_movies, "Popular Movies")

            # Personalized Recommendations
            st.write("### Personalized Recommendations")
            user_id = st.number_input("Enter Your Unique Identifier", min_value=1, step=1)
    
            if st.button("Get Personalized Recommendations"):
                try:
                    user_cf_movies = recom_movies_cf(user_id, num_recommendations)
                    display_movie_cards(user_cf_movies, "Personalized Movies for You!!")
                except KeyError:
                    st.error("Unique Identifier not found")

    # Add some spacing at the bottom
            st.markdown("<br><br>", unsafe_allow_html=True)

        



if __name__ == "__main__":
    main()
