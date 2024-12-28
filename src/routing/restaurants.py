from flask import render_template, redirect, session, flash, request
from app import app
from service.helper_service import add_restaurant
from db_module import get_restaurants_all, get_restaurants_by_id


@app.route("/restaurants")
def restaurants():
    return render_template("restaurants_list.html", restaurants=get_restaurants_all())


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    return render_template("restaurants_single.html", restaurant=restaurant)


@app.route("/restaurants/new")
def create_restaurant_form():
    return render_template("restaurants_new.html")


@app.route("/restaurants/create", methods=["POST"])
def create_restaurant_endpoint():
    if "user_id" not in session or not session["user_id"]:
        flash("Error: You are not logged in.")
        return redirect("/restaurants/new")
    admin_id = session["user_id"]
    new_index, error = add_restaurant(
        admin_id=admin_id, name=request.form["name"], address=request.form["address"]
    )
    if error or not str(new_index).isnumeric or new_index < 1:
        [flash(f"Error: {err}") for err in error]
        return redirect("/restaurants/new")
    flash("Success: Restaurant created.")
    return redirect(f"/restaurants/{new_index}")
