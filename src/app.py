from config import DATABASE_NAME, FLASK_SECRET_KEY
from filters import output_date, output_datetime, output_rating_stars, output_account_name
from flask import Flask
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
if not DATABASE_NAME or not FLASK_SECRET_KEY:
    raise RuntimeError(
        "Please check your env file and its DATABASE_NAME and FLASK_SECRET_KEY."
    )
app.secret_key = FLASK_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg:///" + DATABASE_NAME

app.add_template_filter(output_date, "output_date")
app.add_template_filter(output_datetime, "output_datetime")
app.add_template_filter(output_rating_stars, "output_rating_stars")
app.add_template_filter(output_account_name, "output_account_name")

db = SQLAlchemy(app)


import routes
