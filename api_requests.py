import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL_REQUEST = "http://www.omdbapi.com/"
API_KEY = os.getenv('API_KEY')


def retrieve_movie_data_from_api(movie_title):
    params = {
        "t": movie_title,
        "apikey": API_KEY
    }

    response = requests.get(URL_REQUEST, params=params)
    movie_data = response.json()

    # Check if movie found
    if movie_data.get("Response") == "False":
        return None

    # Map API fields to your DB structure
    return {
        "title": movie_data.get("Title"),
        "director": movie_data.get("Director"),
        "year": int(movie_data.get("Year")) if movie_data.get("Year") else None,
        "poster_url": movie_data.get("Poster")
    }