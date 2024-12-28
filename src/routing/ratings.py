from flask import render_template
from app import app
from db_module import get_ratings_all, get_ratings_by_id

#############################################
#   RATINGS                                 #
#############################################


@app.route("/ratings")
def ratings():
    return render_template("ratings_list.html", ratings=get_ratings_all())


@app.route("/ratings/<int:rating_id>")
def single_rating(rating_id):
    rating = get_ratings_by_id(rating_id)
    return render_template("ratings_single.html", rating=rating)
