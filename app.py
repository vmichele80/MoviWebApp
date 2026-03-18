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
    return "Welcome to MoviWeb App!"

@app.route('/users')
def list_users():
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

if __name__ == '__main__':
  #with app.app_context():
    #db.create_all()

  app.run()