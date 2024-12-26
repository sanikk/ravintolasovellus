from flask import redirect, render_template, request
from app import app

from db_module import get_restaurants_all, get_restaurants_single
from db_module import get_accounts_all
from db_module import get_ratings_all, get_ratings_single

from map_service import get_map


@app.route("/")
def index():
    return render_template("map_page.html", iframe=get_map())


@app.route("/accounts")
def accounts():
    accounts_list = get_accounts_all()
    return render_template("accounts_list.html", accounts=accounts_list)


@app.route("/restaurants")
def restaurants():
    return render_template("restaurants_list.html", restaurants=get_restaurants_all())


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant(restaurant_id):
    name, lat, lng, place_id, address = get_restaurants_single(restaurant_id)
    return render_template(
        "restaurants_single.html",
        name=name,
        lat=lat,
        lng=lng,
        place_id=place_id,
        address=address,
    )


@app.route("/restaurants/new")
def add_restaurant():
    return render_template("restaurants_new.html")


@app.route("/ratings")
def ratings():
    return render_template("ratings_list.html", ratings=get_ratings_all())


@app.route("/ratings/<int:rating_id>")
def single_rating(rating_id):
    rating = get_ratings_single(rating_id)
    return render_template("ratings_single.html", rating=rating)
