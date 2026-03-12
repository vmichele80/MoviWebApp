
from flask import Flask

app = Flask(__name__)



"""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

"""

"""""

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    director TEXT NOT NULL,
    year INTEGER,
    poster_url TEXT
    user_id INTEGER FOREIGN KEY
);
    
"""""
