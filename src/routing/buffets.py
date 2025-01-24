from flask import render_template, redirect, request, session, flash
from app import app
from db_module import (
    create_buffet,
    get_accountId_by_restaurantId,
    get_buffets_all,
    get_buffets_by_id,
    get_restaurants_all,
    update_buffet,
)
from service.validation_service import validate_buffet_data
from calendar import day_name


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
        "buffets_new.html",
        restaurant_id=restaurant_id,
        restaurants=restaurants,
        form_data={},
    )


@app.route("/buffets/create", methods=["POST"])
def create_buffet_endpoint():
    if "user_id" in session:
        chosen_days = request.form.getlist("days")
        user_input = {
            "name": request.form["name"],
            "account_id": session.get("user_id", ""),
            "restaurant_id": request.form["restaurant_id"],
            "days": {day: (day in chosen_days) for day in day_name},
            "starttime": request.form["starttime"],
            "endtime": request.form["endtime"],
            "price": request.form["price"],
            "description": request.form["description"],
        }
        error = validate_buffet_data(user_input)
        if not error:
            ret = create_buffet(**user_input)
            if ret:
                return redirect(f"/buffets/{ret}")
            flash(
                "Error: Something went wrong creating the buffet. No return value from db"
            )
        [flash(err) for err in error]
    else:
        flash("Error: please login first")
    return render_template(
        "buffets_new.html", form_data=request.form, restaurants=get_restaurants_all()
    )


@app.route("/buffets/edit/<int:buffet_id>")
def buffet_edit_form(buffet_id: int):
    buffet = get_buffets_by_id(buffet_id)
    if buffet:
        if buffet.account_id == session["user_id"]:
            return render_template(
                "buffets_edit.html",
                buffet=buffet,
                form_data={},
                restaurants=get_restaurants_all(),
            )
        flash("Error: you are not logged in as admin of this restaurant")
    flash("Error: No such active buffet")
    return redirect("/buffets")


@app.route("/buffets/update/<int:buffet_id>")
def update_buffet_endpoint(buffet_id: int):
    if get_buffets_by_id(buffet_id):
        restaurant_id = request.form.get("restaurant_id", "")
        if restaurant_id and restaurant_id.isnumeric:
            owner_id = get_accountId_by_restaurantId(int(restaurant_id))
            if "user_id" in session and session["user_id"] == owner_id:
                chosen_days = request.form.getlist("days")
                user_input = {
                    "id": buffet_id,
                    "name": request.form["name"],
                    "account_id": session.get("user_id", ""),
                    "restaurant_id": restaurant_id,
                    "days": {day: (day in chosen_days) for day in day_name},
                    "starttime": request.form["starttime"],
                    "endtime": request.form["endtime"],
                    "price": request.form["price"],
                    "description": request.form["description"],
                }
                error = validate_buffet_data(user_input)
                if not error:
                    ret = update_buffet(**user_input)
                    if ret:
                        return redirect(f"/buffets/{ret}")
                    flash(
                        "Error: Something went wrong updating the buffet. No return value from db"
                    )
                [flash(err) for err in error]
            else:
                flash("Error: you are not logged in as the admin of this restaurant")
        else:
            flash("Error: please choose a valid restaurant")
    else:
        flash("Error: no such buffet")
    return render_template(
        "buffets_new.html", form_data=request.form, restaurants=get_restaurants_all()
    )
