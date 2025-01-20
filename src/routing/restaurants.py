from flask import render_template, redirect, session, flash, request
from app import app
from db_module import (
    get_buffets_by_restaurantId,
    get_events_by_restaurantId,
    get_ratings_by_restaurantId,
    get_restaurants_all,
    get_restaurants_by_id,
    get_accountId_by_restaurantId,
    delete_restaurant_by_id,
    update_restaurant_by_id,
    create_restaurant,
)
from service.validation_service import validate_restaurant_data


@app.route("/restaurants")
def restaurants():
    return render_template("restaurants_list.html", restaurants=get_restaurants_all())


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant(restaurant_id):
    restaurant = get_restaurants_by_id(restaurant_id)
    events = get_events_by_restaurantId(restaurant_id)
    buffets = get_buffets_by_restaurantId(restaurant_id)
    ratings = get_ratings_by_restaurantId(restaurant_id)
    return render_template(
        "restaurants_single.html",
        restaurant=restaurant,
        events=events,
        buffets=buffets,
        ratings=ratings,
    )


@app.route("/restaurants/new")
def create_restaurant_form():
    return render_template("restaurants_new.html", form_data={})


@app.route("/restaurants/create", methods=["POST"])
def create_restaurant_endpoint():
    if "user_id" not in session or not session["user_id"]:
        flash("Error: You are not logged in.")
        return redirect("/restaurants/new")
    account_id = session["user_id"]
    name = request.form["name"]
    address = request.form["address"]
    description = request.form["description"]
    lat, long, place_id, error = validate_restaurant_data(
        name, account_id, address, description
    )
    if not error and lat and long and place_id:
        ret = create_restaurant(
            name, account_id, address, lat, long, place_id, description
        )
        if ret:
            flash("Success: Restaurant created.")
            return redirect(f"/restaurants/{ret}")
        error.append("Error: something went wrong in creating the restaurant")
    [flash(err) for err in error]
    return render_template("restaurants_new.html", form_data=request.form)


@app.route("/restaurants/delete/<int:restaurant_id>", methods=["POST"])
def remove_restaurant(restaurant_id: int):
    account_id = get_accountId_by_restaurantId(restaurant_id)
    if account_id:
        if "user_id" in session and session["user_id"] == account_id[0]:
            delete_restaurant_by_id(restaurant_id)
            flash("Restaurant has been deleted.")
            return redirect("/restaurants")
        flash("Error: You are not logged in as the owner of this restaurant.")
        return redirect(f"/restaurants/{restaurant_id}")
    flash("Error: this restaurant does not seem to exist")
    return redirect("/restaurants")


@app.route("/restaurants/edit/<int:restaurant_id>")
def edit_restaurant_form(restaurant_id: int):
    account_id = get_accountId_by_restaurantId(restaurant_id)
    if account_id:
        if "user_id" in session and session["user_id"] == account_id[0]:
            ret = get_restaurants_by_id(restaurant_id)
            if ret and len(ret) == 7:
                form_data = {}
                form_data["name"] = ret[1]
                form_data["address"] = ret[6]
                return render_template(
                    "restaurants_edit.html",
                    form_data=form_data,
                    restaurant_id=restaurant_id,
                )
            flash("Error: Unable to access that restaurant")
            return redirect("/restaurants")

        flash("Error: You are not logged in as the owner of this restaurant.")
        return redirect(f"/restaurants/{restaurant_id}")

    flash("Error: this restaurant does not seem to exist")
    return redirect("/restaurants")


@app.route("/restaurants/update/<int:restaurant_id>", methods=["POST"])
def update_restaurant_endpoint(restaurant_id: int):
    account_id = get_accountId_by_restaurantId(restaurant_id)
    if account_id:
        account_id = account_id[0]
        if "user_id" in session and session["user_id"] == account_id:
            name = request.form["name"]
            address = request.form["address"]
            description = request.form["description"]
            lat, long, place_id, error = validate_restaurant_data(
                name, account_id, address, description
            )
            if lat and long and place_id and not error:
                update_restaurant_by_id(
                    restaurant_id, name, address, lat, long, place_id, description
                )
                flash("Restaurant data updated.")
                return redirect(f"/restaurants/{restaurant_id}")
            [flash(err) for err in error]
            return render_template(
                "restaurants_edit.html",
                form_data=request.form,
                restaurant_id=restaurant_id,
            )
        flash("Error: You are not logged in as the owner of this restaurant.")
        return redirect(f"/restaurants/{restaurant_id}")

    flash("Error: this restaurant does not seem to exist")
    return redirect("/restaurants")
