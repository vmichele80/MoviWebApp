from models import db, User, Movie

class DataManager():
    # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)

        db.session.add(new_user)
        db.session.commit()

    # there is no function for deleting users
    # Why that??

    def get_user(self, name):
        # Return a list of all users in your database.
        pass


    def get_movie(self, user_id):
        # Return a list of all movies of a specific user.
        pass


    def add_movie(self, movie):
        # Add a new movie to a user’s favorites.
        # The process is similar to adding a new user.
        new_movie = Movie(
            title = movie["title"],
            director = movie["director"],
            year = movie["year"],
            post_url = movie["post_url"],
            user_id = movie["user_id"]
        )
        db.session.add(new_movie)
        db.session.commit()



        # Consider for later
        # Use the title parameter passed instead of movie
        # to query the IMDB api (fuzzy search)
        # and save the response into the DB

        # the movie id is created automatically
        # the user_id comes from the user who is adding this movie
        pass



    def update_movie(self, movie_id, new_title):
        # Update the details of a specific movie in the database.
        pass

    def delete_movie(self, movie_id):
        # Delete the movie from the user’s list of favorites.
        movie_to_delete = Movie.query.get_or_404(movie_id)

        db.session.delete(movie_to_delete)
        db.session.commit()
        pass


