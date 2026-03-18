from flask import Flask, request
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)



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
def home():
    """
    The home page of your application. Show a list of all registered
    users and a form for adding new users. (This route is GET by default.)
    """
    return "Welcome to MoviWeb App!"

@app.route('/users', methods=['POST'])
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


@app.route("/add_user")
def add_user():
    name = request.args.get("name")

    if not name:
        return "Provide a name"

    user = data_manager.create_user(name)
    return f"Created user {user.id}: {user.name}"

@app.route("/update_user")
def update_user():
    user_id = request.args.get("user_id")
    new_name = request.args.get("name")

    if not user_id or not new_name:
        return "Use /update_user?user_id=2&name=Anna"

    updated_user = data_manager.update_user(int(user_id), new_name)

    if updated_user is None:
        return "User not found"

    return f"Updated user: {updated_user.id}: {updated_user.name}"

@app.route('/users/<int:user_id>/movies', methods=['GET'])
    def get_list_of_users_favorites():
    """When you click on a user name, the app retrieves that user’s list of
    favorite movies and displays it."""
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
    def add_movie_to_favorites():
    """
    Add a new movie to a user’s list of favorite movies.
    """
    #here we need furthermore to fetch the information from the IMDb service
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
    def update_movie():
    """
    Modify the title of a specific movie in a user’s list, without depending 
    on OMDb for corrections.
    """
    pass

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST']
    def delete_movie():
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    pass


if __name__ == '__main__':
  #with app.app_context():
    #db.create_all()

  app.run()