from flask import render_template, redirect, request, session, flash
from app import app
from db_module import (
    create_buffet,
    get_buffets_all,
    get_buffets_by_id,
    get_restaurants_all,
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
    return render_template(
        "buffets_new.html", form_data=request.form, restaurants=get_restaurants_all()
    )
