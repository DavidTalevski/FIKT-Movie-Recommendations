from src.movieDatabases import MovieDatabase
import inquirer
from src.user import User
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def ask_user_for_favorite_actors():
    actor_question = inquirer.Text(
        "favorite_actors",
        message="Enter the names of your favorite actors (comma-separated, e.g., Tom Hanks, Meryl Streep)",
    )

    actor_answers = inquirer.prompt([actor_question])["favorite_actors"]

    # Check if actor_answers is empty and return an empty list if so
    if not actor_answers:
        return []

    return [actor.strip() for actor in actor_answers.split(",")]

def ask_user_for_years():
    year_choices = db.years.copy()
    year_choices.insert(0, "All")

    year_question = inquirer.Checkbox(
        "selected_years",
        message="Select the years you're interested in for movies:",
        choices=year_choices,
    )

    year_answers = inquirer.prompt([year_question])["selected_years"]

    if year_answers:
        if "All" in year_answers:
            return db.years  # User selected "All," so include all years
        elif len(year_answers) > 0:
            return year_answers

    return db.years


def ask_user_for_genres():
    genre_question = inquirer.Checkbox(
        "genres", message="Which genres are you interested in?", choices=db.genres
    )

    genre_answers = inquirer.prompt([genre_question])["genres"]

    return genre_answers if genre_answers else []

def view_movies_one_by_one(movies, genres, cast):
    total_movies = len(movies)
    for index, movie in enumerate(movies, start=1):
        print("\n-------------------------------")
        print(f"Viewing movie {index} out of {total_movies}")
        print("Title:", movie["title"])
        print("Release Year:", movie["year"])
        
        # Print genres with matching argument genres in green, and the rest in the default color
        genre_str = ", ".join([Fore.GREEN + g + Fore.RESET if g in genres else g for g in movie["genres"]])
        print("Genres:", genre_str)
        print("Description:", movie.get("extract", "No information."))
        
        # Print cast with matching cast names in green, and the rest in the default color
        cast_str = ", ".join([Fore.GREEN + actor + Fore.RESET if actor in cast else actor for actor in movie["cast"]])
        print("Cast:", cast_str)
        
        print("-------------------------------\n")
        
        user_input = input("Press Enter to view the next movie or 'q' to quit: ")
        
        if user_input.lower() == 'q':
            break

if __name__ == "__main__":
    db = MovieDatabase()
    db.load_data()

    user = User()

    user.selected_years = ask_user_for_years()
    user.favorite_genres = ask_user_for_genres()
    user.favorite_actors = ask_user_for_favorite_actors()

    filtered_movies = db.filter_movies(user.selected_years, user.favorite_genres, user.favorite_actors)
    
    if not filtered_movies:
        print("No movies match your criteria.")
    else:
        print(f"Found {len(filtered_movies)} movies that match your criteria.")
        view_movies_one_by_one(filtered_movies, user.favorite_genres, user.favorite_actors)