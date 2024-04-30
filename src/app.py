from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg:///' + getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


import routes
