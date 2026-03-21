from flask import Flask, request, render_template, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie
from api_requests import retrieve_movie_data_from_api
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"



basedir = os.path.abspath(os.path.dirname(__file__))
# this creates the data folder if it does not exist
os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

# if data folder does not exist, the db creation will fail
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

with app.app_context():
    db.create_all()
    print("Tables created.")



@app.route('/')
def index():
    """
    The home page of your application. Show a list of all registered
    users and a form for adding new users. (This route is GET by default.)
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)

# potentially to be removes as not used. but let's see
@app.route('/users', methods=['GET'])
def list_users():
    """
    When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database, then
    redirects back to /.
    """
    users = data_manager.get_users()
    if not users:
        return "No users found"

    return "<br>".join([f"{user.id}: {user.name}" for user in users])


@app.route("/users", methods=['POST'])
def create_user():
    """
    When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database, then
    redirects back to /
    """
    name = request.form.get("name")

    if not name:
        return "Provide a name"

    """    
    # need to change to make it behave properly as an endpoint
    # this was useful for testing
    user = data_manager.create_user(name)
    return f"Created user {user.id}: {user.name}"
    """

    #creates the new user
    data_manager.create_user(name)
    # redirect to the index page so that the new added user can be seen
    return redirect(url_for('index'))

@app.route("/update_user", methods=['POST'])
def update_user():
    """
    It updates details about the user in case of misspellings
    """

    user_id = request.form.get("user_id")
    new_name = request.form.get("name")

    if not user_id or not new_name:
        return "Provide user_id and name"

    updated_user = data_manager.update_user(int(user_id), new_name)

    if updated_user is None:
        return "User not found"

    return f"Updated user: {updated_user.id}: {updated_user.name}"



@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_list_of_users_favorites(user_id):
    """When you click on a user name, the app retrieves that user’s list of
    favorite movies and displays it."""
    movies = data_manager.get_movies(user_id)

    # if not movies:
    #    return f"No favorite movies found for user {user_id}"

    return render_template('movies.html', movies=movies, user_id=user_id)

    """
    # This was good only for testing purposes. Remove before publishing
    return "<br>".join([
        f"{movie.id}: {movie.title} - {movie.director} ({movie.year})"
        for movie in movies
    ])
    """


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_favorites(user_id):
    """
    Add a new movie to a user’s list of favorite movies.
    """
    movie_title = request.form.get("title")

    if not movie_title:
        flash("Please provide a movie title.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    # here we need furthermore to fetch the information from the IMDb service
    movie_data = retrieve_movie_data_from_api(movie_title)

    if movie_data is None:
        flash("Movie not found.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    movie_data["user_id"] = user_id
    #now movie_data is complete and can be passed over the function
    data_manager.add_movie(movie_data)

    flash(f"Movie '{movie_data['title']}' added successfully.")
    return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    # This was for testing when no UI was implemented
    # return f"Added movie: {new_movie.id}: {new_movie.title}"



@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list, without depending
    on OMDb for corrections.
    """
    new_title = request.form.get("title")

    if not new_title:
        flash("Please provide a new title.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    updated_movie = data_manager.update_movie(movie_id, {"title": new_title})

    if updated_movie is None:
        flash("Movie not found.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    # Checks if movie belongs to this user favorites
    if updated_movie.user_id != user_id:
        flash("Movie does not belong to this user.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    flash(f"Movie updated to '{updated_movie.title}'.")
    return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    # This was good for BE testing when no UI was available
    # return f"Updated movie: {updated_movie.id}: {updated_movie.title}"

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    movies = data_manager.get_movies(user_id)
    movie_to_delete = None

    for movie in movies:
        if movie.id == movie_id:
            movie_to_delete = movie
            break

    if movie_to_delete is None:
        flash("Movie not found for this user.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    movie_title = movie_to_delete.title

    success = data_manager.delete_movie(movie_id)

    if not success:
        flash("Movie could not be deleted.")
        return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    flash(f"Movie '{movie_title}' deleted successfully.")
    return redirect(url_for('get_list_of_users_favorites', user_id=user_id))

    # Good for BE, now with UI we do not need it anymore
    # return f"Deleted movie '{movie_title}' from user {user_id}'s favorites"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    # This has been moved out at the beginning of the file
    # as was creating problems with the db creation

    # with app.app_context():
    # db.create_all()
  app.run()