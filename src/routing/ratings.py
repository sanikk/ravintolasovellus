from flask import render_template, redirect, request
from app import app
from db_module import (
    get_ratings_all,
    get_ratings_by_id,
    get_restaurants_all,
    get_restaurants_by_id,
)

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


@app.route("/ratings/new")
def new_rating_form():
    restaurants = get_restaurants_all()
    preselected_restaurant = None
    restaurant_id = request.args.get("restaurant_id")
    if restaurant_id and restaurant_id.isnumeric():
        preselected_restaurant = get_restaurants_by_id(int(restaurant_id))
    return render_template(
        "ratings_new.html",
        restaurants=restaurants,
        preselected_restaurant=preselected_restaurant,
    )


@app.route("/ratings/create", methods=["POST"])
def create_rating_endpoint():
    return redirect("/ratings")
