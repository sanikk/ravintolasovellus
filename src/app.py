from flask import Flask
from flask import redirect, render_template, request
from os import getenv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map_view():
    return render_template("map.html")
