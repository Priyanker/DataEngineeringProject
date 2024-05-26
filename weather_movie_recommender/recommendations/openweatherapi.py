# -*- coding: utf-8 -*-
"""OpenWeatherAPI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MMTM9TmgGLw79Earz3dlzO9YlBf_dZ--

# Open Weather API
"""

import datetime as dt
import requests

"""# Weather Conditions Mapping
Initialize a dictionary to map OpenWeather API condition IDs to their descriptive strings, enabling detailed weather analysis in conjunction with our movie dataset.

https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
"""

weather_conditions = {
    "Thunderstorm": {
        200: "thunderstorm with light rain",
        201: "thunderstorm with rain",
        202: "thunderstorm with heavy rain",
        210: "light thunderstorm",
        211: "thunderstorm",
        212: "heavy thunderstorm",
        221: "ragged thunderstorm",
        230: "thunderstorm with light drizzle",
        231: "thunderstorm with drizzle",
        232: "thunderstorm with heavy drizzle",
    },
    "Drizzle": {
        300: "light intensity drizzle",
        301: "drizzle",
        302: "heavy intensity drizzle",
        310: "light intensity drizzle rain",
        311: "drizzle rain",
        312: "heavy intensity drizzle rain",
        313: "shower rain and drizzle",
        314: "heavy shower rain and drizzle",
        321: "shower drizzle",
    },
    "Rain": {
        500: "light rain",
        501: "moderate rain",
        502: "heavy intensity rain",
        503: "very heavy rain",
        504: "extreme rain",
        511: "freezing rain",
        520: "light intensity shower rain",
        521: "shower rain",
        522: "heavy intensity shower rain",
        531: "ragged shower rain",
    },
    "Snow": {
        600: "light snow",
        601: "Snow",
        602: "Heavy snow",
        611: "Sleet",
        612: "Light shower sleet",
        613: "Shower sleet",
        615: "Light rain and snow",
        616: "Rain and snow",
        620: "Light shower snow",
        621: "Shower snow",
        622: "Heavy shower snow",
    },
    "Atmosphere": {
        701: "mist",
        711: "Smoke",
        721: "Haze",
        731: "sand/dust whirls",
        741: "fog",
        751: "sand",
        761: "dust",
        762: "volcanic ash",
        771: "squalls",
        781: "tornado",
    },
    "Clear": {
        800: "clear sky",
    },
    "Clouds": {
        801: "few clouds",
        802: "scattered clouds",
        803: "broken clouds",
        804: "overcast clouds",
    },
}

icon_list = {
    "clear sky": {
        "day": "01d.png",
        "night": "01n.png"
    },
    "few clouds": {
        "day": "02d.png",
        "night": "02n.png"
    },
    "scattered clouds": {
        "day": "03d.png",
        "night": "03n.png"
    },
    "broken clouds": {
        "day": "04d.png",
        "night": "04n.png"
    },
    "shower rain": {
        "day": "09d.png",
        "night": "09n.png"
    },
    "rain": {
        "day": "10d.png",
        "night": "10n.png"
    },
    "thunderstorm": {
        "day": "11d.png",
        "night": "11n.png"
    },
    "snow": {
        "day": "13d.png",
        "night": "13n.png"
    },
    "mist": {
        "day": "50d.png",
        "night": "50n.png"
    }
}

"""# Movies Dataset Transformations

# Loading the movie datasets

Loading the genre movie datasets
"""
class WeatherMovieRecommender:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "ENTER_YOUR_API_KEY_HERE"  # Ideally, load this from environment variables or a config file

    def __init__(self, city):
        self.city = city
        
        
        genre_files = {
            'action': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/action.csv',
            'adventure': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/adventure.csv',
            'animation': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/animation.csv',
            'biography': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/biography.csv',
            'crime': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/crime.csv',
            'family': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/family.csv',
            'fantasy': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/fantasy.csv',
            'film-noir': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/film-noir.csv',
            'history': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/history.csv',
            'horror': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/horror.csv',
            'mystery': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/mystery.csv',
            'romance': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/romance.csv',
            'scifi': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/scifi.csv',
            'sports': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/sports.csv',
            'thriller': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/thriller.csv',
            'war': 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/GenreMoviesDatasets/war.csv',
        }


        import pandas as pd
        # Dictionary to hold dataframes
        genre_dfs = {}

        # Loading genre datasets
        for genre, url in genre_files.items():
            genre_dfs[genre] = pd.read_csv(url)

        # First few rows of the action dataframe
        print(genre_dfs['action'].head())

        print("Columns of the Genre DataFrame:", genre_dfs['action'].columns)

        """Loading the movie metadata datasets"""

        metadata_url = 'https://raw.githubusercontent.com/Priyanker/DataEngProjectDatasets/main/MoviesMetadata/movies_metadata.csv'
        movies_metadata_df = pd.read_csv(metadata_url)

        print(movies_metadata_df.head())
        print("Length of DataFrame:", len(movies_metadata_df))

        print("Columns of the Movie Metadata DataFrame:", movies_metadata_df.columns)

        """# Merging the genre and movie metadata datasets

        Checking if the movie_id and imdb_id are in the same format
        """

        print(genre_dfs['action']['movie_id'].dtype)
        print(movies_metadata_df['imdb_id'].dtype)

        """Merge the genre and movie metadata dataset by joining the movie_id from the genre datasets and imdb_id from the metadata datasets.

        Merge only if there's a matching movie_id in the metadata dataset - Inner Join. (Removing movies with no metadata. These are relatively unkown movies with not a lot of information and not useful for analysis)
        """

        def merge_with_metadata(genre_df, metadata_df):
            merged_df = genre_df.merge(metadata_df, how='inner', left_on='movie_id', right_on='imdb_id')
            merged_df.drop(columns=['imdb_id', 'gross(in $)', 'star_id', 'director_id', 'poster_path', 'runtime_y', 'video', 'vote_count', 'vote_average'], inplace=True)
            merged_df.rename(columns={'runtime_x': 'runtime'}, inplace=True)
            return merged_df

        merged_genre_dfs = {}

        for genre, df in genre_dfs.items():
            merged_genre_dfs[genre] = merge_with_metadata(df, movies_metadata_df)

        print(merged_genre_dfs['action'].head())

        print("Columns of the merged genre DataFrame:", merged_genre_dfs['action'].columns)

        df = merged_genre_dfs['action']
        print(df.dtypes)

        """Data type conversions

        Looping through all merged genre DataFrames and saving them as CSV files
        """

        import json
        for genre, df in merged_genre_dfs.items():
            # Convert 'year' column to numeric, coercing errors into NaNs
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            # Convert to pandas' nullable integer type
            df['year'] = df['year'].astype('Int64')

            # Remove ' min' from the runtime_x column and convert to numeric
            df['runtime'] = df['runtime'].str.replace(' min', '').astype('float').astype('Int64')

            # Convert 'votes' column to Int64, allowing for NaN values
            df['votes'] = pd.to_numeric(df['votes'], errors='coerce').astype('Int64')

            # Normalize the case and convert 'adult' column to boolean
            df['adult'] = df['adult'].str.lower().map({'true': True, 'false': False, 'yes': True, 'no': False, '1': True, '0': False}).astype('boolean')

            # Function to safely convert single-quoted strings to valid JSON
            def safe_json_loads(s):
                try:
                    return json.loads(s.replace("'", '"'))
                except json.JSONDecodeError:
                    # Log the error
                    return []

            # Function to merge genres
            def merge_genres(row):
                # Parse the 'genres' column with safe_json_loads to handle single quotes
                genres_list = safe_json_loads(row['genres'])

                # Extract genre names and form a set for uniqueness
                new_genres = {genre['name'] for genre in genres_list if genre and 'name' in genre}

                # Split existing 'genre' field and form a set
                existing_genres = set(row['genre'].split(', '))

                # Combine the sets, convert to sorted list to maintain order, then join back into a string
                all_genres = sorted(existing_genres.union(new_genres))
                return ', '.join(all_genres)

            # Apply the function to merge genres and update the 'genre' column
            df['genre'] = df.apply(merge_genres, axis=1)

            # Remove the 'genres' column
            df.drop('genres', axis=1, inplace=True)


            # Function to extract names and convert to a comma-separated string
            def extract_names(json_string):
                # Parse the JSON string with safe_json_loads to handle single quotes
                json_data = safe_json_loads(json_string)
                # Extract the 'name' values
                names = [entry['name'] for entry in json_data if 'name' in entry]
                # Join the names into a comma-separated string
                return ', '.join(names)

            # Apply the function to each relevant column
            df['production_companies'] = df['production_companies'].apply(extract_names)
            df['production_countries'] = df['production_countries'].apply(extract_names)
            df['spoken_languages'] = df['spoken_languages'].apply(extract_names)

            # Convert 'release_date' column to datetime, coercing errors into NaT
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

            # Filter out records where (budget = 0 OR revenue = 0) AND votes < 1000
            df = df[~(((df['budget'] == 0) | (df['revenue'] == 0)) & (df['votes'] < 3000))]

            # After conversions, you can optionally save the progress again
            # df.to_csv(f'{genre}_merged_cleaned.csv', index=False)


        """# Weather - Genre Mapping"""

        weather_genre_mapping = {
            "thunderstorm with light rain": ["thriller", "horror"],
            "thunderstorm with rain": ["thriller", "horror", "mystery"],
            "thunderstorm with heavy rain": ["thriller", "mystery", "film-noir"],
            "light thunderstorm": ["thriller", "horror"],
            "thunderstorm": ["action", "thriller", "horror"],
            "heavy thunderstorm": ["action", "thriller"],
            "ragged thunderstorm": ["horror", "thriller"],
            "thunderstorm with light drizzle": ["romance", "mystery"],
            "thunderstorm with drizzle": ["mystery", "film-noir"],
            "thunderstorm with heavy drizzle": ["film-noir", "mystery"],

            "light intensity drizzle": ["romance"],
            "drizzle": ["romance", "animation"],
            "heavy intensity drizzle": ["mystery"],
            "light intensity drizzle rain": ["romance"],
            "drizzle rain": ["romance", "mystery"],
            "heavy intensity drizzle rain": ["mystery", "thriller"],
            "shower rain and drizzle": ["romance"],
            "heavy shower rain and drizzle": ["thriller", "mystery"],
            "shower drizzle": ["romance"],

            "light rain": ["romance"],
            "moderate rain": ["romance", "mystery"],
            "heavy intensity rain": ["thriller", "mystery"],
            "very heavy rain": ["thriller", "film-noir"],
            "extreme rain": ["thriller", "adventure"],
            "freezing rain": ["romance"],
            "light intensity shower rain": ["romance"],
            "shower rain": ["romance", "mystery"],
            "heavy intensity shower rain": ["thriller", "mystery"],
            "ragged shower rain": ["mystery", "thriller"],

            "light snow": ["family", "fantasy"],
            "snow": ["family", "fantasy"],
            "heavy snow": ["family", "fantasy"],
            "sleet": ["family"],
            "light shower sleet": ["family", "animation"],
            "shower sleet": ["family"],
            "light rain and snow": ["romance", "family"],
            "rain and snow": ["romance", "family"],
            "light shower snow": ["family"],
            "shower snow": ["family"],
            "heavy shower snow": ["thriller", "adventure"],

            "mist": ["mystery", "thriller"],
            "smoke": ["history", "biography"],
            "haze": ["mystery", "biography"],
            "sand/dust whirls": ["adventure", "history"],
            "fog": ["mystery", "thriller"],
            "sand": ["adventure"],
            "dust": ["adventure"],
            "volcanic ash": ["adventure"],
            "squalls": ["thriller"],
            "tornado": ["thriller"],

            "clear sky": ["adventure", "action", "sports"],

            "few clouds": ["family", "animation"],
            "scattered clouds": ["biography"],
            "broken clouds": ["mystery", "thriller"],
            "overcast clouds": ["film-noir", "war"]
        }

        """# Recommending movies based on weather conditions

        # Getting the API Response
        """

        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        import os
        API_KEY = os.getenv('API_KEY')


        url = BASE_URL + "appid=" + API_KEY + "&q=" + self.city

        self.weather_response = requests.get(url).json()
        print(self.weather_response)

        def suggest_movies(weather_response, weather_genre_mapping, genre_dfs):
            # Extract the weather description from the response
            weather_description = weather_response['weather'][0]['description'].lower()

            # Find the matching genres for this weather description
            matched_genres = weather_genre_mapping.get(weather_description, [])

            # Dictionary to hold the top 5 suggestions from each matched genre DataFrame
            top_suggestions_per_genre = {}

            # Fetch the top 5 movies from the dataframes of these genres
            for genre in matched_genres:
                genre_key = genre.lower()
                if genre_key in genre_dfs:
                    # Get the DataFrame for the current genre
                    genre_df = genre_dfs[genre_key]
                    # Sort by multiple criteria, such as 'rating', 'votes', and 'release_date'
                    top_movies = genre_df.sort_values(by=['votes', 'rating', 'revenue', 'release_date', 'popularity'], ascending=[False, False, False, False, False]).head(5)
                    top_suggestions_per_genre[genre] = top_movies

            return top_suggestions_per_genre
        
                
        # Use the function to get movie suggestions
        self.movie_suggestions_list = suggest_movies(self.weather_response, weather_genre_mapping, merged_genre_dfs)

    def get_icon_for_condition(weather_id):
        # A mapping of weather condition codes to the closest available icons
        weather_to_icon_mapping = {
            "Thunderstorm": "thunderstorm",
            "Drizzle": "rain",
            "Rain": "shower rain",
            "Snow": "snow",
            "Atmosphere": "mist",
            "Clear": "clear sky",
            "Clouds": "scattered clouds",
        }

        # A mapping from weather condition codes to broader categories
        code_to_category = {
            range(200, 300): "Thunderstorm",
            range(300, 400): "Drizzle",
            range(500, 600): "Rain",
            range(600, 700): "Snow",
            range(701, 781): "Atmosphere",
            800: "Clear",
            range(801, 805): "Clouds",
        }

        # Determine the category for the weather_id
        category = None
        for codes, cat in code_to_category.items():
            if isinstance(codes, range) and weather_id in codes:
                category = cat
                break
            elif isinstance(codes, int) and weather_id == codes:
                category = cat
                break

        # Fallback to the closest icon for the category
        closest_icon_description = weather_to_icon_mapping.get(category, "clear sky")
        return icon_list[closest_icon_description]

    # weather_id = 711  # Example weather condition code
    # icon = get_icon_for_condition(weather_id)
    # print(icon)

    def get_weather_data(self):
        return self.weather_response
    
    def generate_movie_recommendations(self):
        return self.movie_suggestions_list
        