from flask import redirect, render_template, request
from app import app

from db_module import get_all_restaurants, get_single_restaurant
from db_module import get_all_accounts

from map_service import get_map


@app.route("/")
def index():
    return render_template("map_page.html", iframe=get_map())


@app.route("/accounts")
def accounts():
    accounts_list = get_all_accounts()
    return render_template("list_accounts.html")


@app.route("/restaurants")
def restaurants():
    return render_template("list_restaurants.html", restaurants=get_all_restaurants())


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant(restaurant_id):
    name, lat, lng = get_single_restaurant(restaurant_id)
    return render_template("single_restaurant.html", name=name, lat=lat, lng=lng)


