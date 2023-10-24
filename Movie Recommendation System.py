# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 08:47:59 2023

"""

import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Load the models

#title - content based
movies = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project/movies_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project/similarity.pkl", 'rb'))

#genre - content based
genre_sim = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project 3/genre_cosine_sim.pkl", 'rb'))
genre_movies = pickle.load(open("C:/Users/Azmarah Rizvi/Desktop/IRWA Project 3/genre_movie_list.pkl", 'rb'))

movies_list = movies['title'].values


# fetch the posters
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=80321b186ae2ff767c6ef9499a9bae85&language=en-US".format(movie_id)
    data = requests.get(url)

    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


# Title - Content based - recommendation function
def recommend(movie):
    # Get the each index and access the title of each movie
    index = movies[movies['title'] == movie].index[0]
    
    # create a list of similarity
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])

    # store the recommended movies inside a list
    recommend_movie = []
    
    # store the movie posters inside a list
    recommend_poster = []
    
    for i in distance[1:6]:
        
        #for posters
        movies_id = movies.iloc[i[0]].id
        recommend_poster.append(fetch_poster(movies_id))
        
        recommend_movie.append(movies.iloc[i[0]].title)
        
    return recommend_movie, recommend_poster

# Genre - content based
def recommend_movies_genres(genre_string, genre_sim=genre_sim):
    # Convert the comma-separated string of genres to a list
    genres = [genre.strip() for genre in genre_string.split(',')]

    # Get the indices of movies that have all of the selected genres
    genre_indices = genre_movies[genre_movies['genre'].apply(lambda x: all(genre in x for genre in genres))].index

    # Sort movies based on 'vote_average' in descending order
    sorted_indices = genre_movies.loc[genre_indices].sort_values(by='vote_average', ascending=False).index

    # Return the top 5 highest-rated movies that fall into all selected genres
    return genre_movies.loc[sorted_indices[:5], ['id', 'title', 'vote_average']]


st.markdown("<h1 style='text-align: center;'>Movie Recommendation System</h1>", unsafe_allow_html=True)

imageCarouselComponent = components.declare_component("image-carousel-component", path="C:/Users/Azmarah Rizvi/Desktop/IRWA Project/frontend/public")


imageUrls = [
    fetch_poster(238),
    fetch_poster(129),
    fetch_poster(105),
    fetch_poster(8587),
    fetch_poster(296096),
    fetch_poster(603),
    fetch_poster(379170),
    fetch_poster(16390),
    fetch_poster(490),
    fetch_poster(597),
    fetch_poster(585),
    fetch_poster(674),
    fetch_poster(399566)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)

def main():  
    # Title - content based
    selectvalue = st.selectbox("Select a Movie Title :", movies_list)

    if st.button("Show Recommend"):
        movie_name, movie_poster = recommend(selectvalue)
        #display
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_name[0])
            if movie_poster[0] is not None:
               st.image(movie_poster[0])
            else:
               st.warning("Poster not available")
        with col2:
            st.text(movie_name[1]) 
            if movie_poster[1] is not None:
               st.image(movie_poster[1])
            else:
               st.warning("Poster not available")
        with col3:
            st.text(movie_name[2])
            if movie_poster[2] is not None:
               st.image(movie_poster[2])
            else:
               st.warning("Poster not available")
        with col4:
            st.text(movie_name[3])
            if movie_poster[3] is not None:
               st.image(movie_poster[3])
            else:
               st.warning("Poster not available")
        with col5:
            st.text(movie_name[4])
            if movie_poster[4] is not None:
               st.image(movie_poster[4])
            else:
               st.warning("Poster not available")

    # genre-based recommendation

    # selecting genres
    selected_genre = st.selectbox('Select a genre :', genre_movies['genre'].str.split(', ').explode().unique())

    # Button for genre-based recommendation
    if st.button("Get Genre Recommendations"):
        # Call the recommend_movies_genres function with all required arguments
        filtered_movies_genre = recommend_movies_genres(selected_genre)
        
        if not filtered_movies_genre.empty:
            # Display posters for recommended movies
            row_posters = st.columns(5)
            
            for idx, (_, movie_row) in enumerate(filtered_movies_genre.head(5).iterrows(), start=1):
                movie_title = movie_row['title']
                vote_average = movie_row['vote_average']
                
                # Fetch poster path using the movie ID
                poster_path = fetch_poster(movie_row['id'])
                
                # Display posters, title, and vote average in a single row
                with row_posters[idx - 1]:
                    st.image(poster_path, caption=f"{movie_title} | IMDb : {vote_average}", use_column_width=True)
        else:
            st.warning('No movies found for the selected genre.')


   
if __name__ == "__main__":
    main()


