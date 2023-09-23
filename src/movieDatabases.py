import os
import json

class MovieDatabase:
    def __init__(self, folder_path="database"):
        self.folder_path = folder_path
        self.data = {}
        self.genres = []
        self.years = [f"{decade}s" for decade in range(1900, 2030, 10)]

    def load_data(self):
        # Load genres from genres.json
        genres_file_path = os.path.join(self.folder_path, "genres.json")
        if os.path.exists(genres_file_path):
            with open(genres_file_path, 'r', encoding="utf8") as genres_file:
                self.genres = json.load(genres_file)
        else:
            print("Warning: Genres file 'genres.json' not found.")
        
        # Load movie data by decade
        for decade in range(1900, 2030, 10):
            filename = f"movies-{decade}s.json"
            file_path = os.path.join(self.folder_path, filename)

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding="utf8") as file:
                    self.data[f"{decade}s"] = json.load(file)
            else:
                print(f"Warning: File '{filename}' not found.")

    def get_movies_by_decade(self, decade):
        return self.data.get(decade, [])

    def filter_movies(self, years, genres, cast):
        merged_movies = []

        for year in years:
            movies_by_decade = self.get_movies_by_decade(year)
            merged_movies.extend(movies_by_decade)

        print(f"Found {len(merged_movies)} movies with the year criteria")

        # Reverse in order for the latest movies to have a higher priority
        merged_movies.reverse();

        filtered_movies = []

        for movie in merged_movies:
            count = 0
            for genre in movie['genres']:
                if genre in genres:
                    count += 1
            movie['count'] = count

        # Filter movies based on genre count
        filtered_movies = [movie for movie in merged_movies if movie['count'] > 0]

        # Filter movies by cast if the cast array is not empty
        if not cast:
            cast_filtered = filtered_movies
        else:
            cast_filtered = [movie for movie in filtered_movies if any(actor in movie['cast'] for actor in cast)]

        print(f"Reduced down to {len(cast_filtered)} movies after applying cast filter")

        # Sort movies by amount of genres
        return sorted(cast_filtered, key=lambda x: x['count'], reverse=True)

