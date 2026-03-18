from models import db, User, Movie

class DataManager:
    # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    # there is no function for deleting users
    # Why that??

    def get_users(self):
        # Return a list of all users in your database.
        return User.query.all()



    def get_movies(self, user_id):
        # Return a list of all movies of a specific user.
        return Movie.query.filter_by(user_id=user_id).all()



    def add_movie(self, movie):
        # Add a new movie to a user’s favorites.
        # The process is similar to adding a new user.
        # I choose to fetch the API data within the app.py
        # and pass it as a movie dictionary
        new_movie = Movie(
            title = movie["title"],
            director = movie["director"],
            year = movie["year"],
            poster_url = movie["poster_url"],
            user_id = movie["user_id"]
        )
        db.session.add(new_movie)
        db.session.commit()

        return new_movie


        # Consider for later
        # Use the title parameter passed instead of movie
        # to query the IMDB api (fuzzy search)
        # and save the response into the DB

        # the movie id is created automatically
        # the user_id comes from the user who is adding this movie

    def update_movie(self, movie_id, updated_data):
        movie = Movie.query.get(movie_id)
        if movie is None:
            return None

        allowed_fields = {"title", "director", "year", "poster_url"}

        for key, value in updated_data.items():
            if key in allowed_fields:
                setattr(movie, key, value)

        db.session.commit()
        return movie


    def delete_movie(self, movie_id):
        # Delete the movie from the user’s list of favorites.
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete is None:
            return False

        db.session.delete(movie_to_delete)
        db.session.commit()
        return True


