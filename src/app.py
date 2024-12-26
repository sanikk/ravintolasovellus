from config import DATABASE_NAME, FLASK_SECRET_KEY
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
if not DATABASE_NAME or not FLASK_SECRET_KEY:
    raise RuntimeError(
        "Please check your env file and its DATABASE_NAME and FLASK_SECRET_KEY."
    )
app.secret_key = FLASK_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg:///" + DATABASE_NAME
db = SQLAlchemy(app)


import routes
