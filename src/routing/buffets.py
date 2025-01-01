from flask import render_template, redirect, request
from app import app
from db_module import get_buffets_all, get_buffets_by_id, get_restaurants_all


@app.route("/buffets")
def buffets_list_page():
    buffets = get_buffets_all()
    return render_template("buffets_list.html", buffets=buffets)


@app.route("/buffets/<int:buffet_id>")
def single_buffet_page(buffet_id: int):
    buffet = get_buffets_by_id(buffet_id)
    return render_template("buffets_single.html", buffet=buffet)


@app.route("/buffets/new")
def new_buffet_form():
    restaurant_id = request.args.get("restaurant_id")
    restaurants = get_restaurants_all()
    return render_template(
        "buffets_new.html", restaurant_id=restaurant_id, restaurants=restaurants
    )


@app.route("/buffets/create", methods=["POST"])
def create_buffet_endpoint():
    # TODO: fill this
    return redirect("/")
