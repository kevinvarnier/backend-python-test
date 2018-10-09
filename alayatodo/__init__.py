from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/alayatodo.db'
PER_PAGE = 5


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
import alayatodo.views


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()