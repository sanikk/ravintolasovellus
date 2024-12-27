from flask import flash, redirect, render_template, request, session
from app import app

from db_module import (
    get_restaurants_all,
    get_restaurants_single,
)
from db_module import (
    get_accounts_all,
    check_username_and_password,
    get_account_by_user_id,
)
from db_module import get_ratings_all, get_ratings_single

from map_service import get_map
from service.helper_service import add_restaurant, add_user


@app.route("/")
def index():
    return render_template("map_page.html", iframe=get_map())


@app.route("/accounts")
def accounts():
    accounts_list = get_accounts_all()
    return render_template("accounts_list.html", accounts=accounts_list)


@app.route("/accounts/<int:user_id>")
def accounts_single(user_id: int):
    account = get_account_by_user_id(user_id)
    return render_template("accounts_single.html", account=account)


@app.route("/accounts/registration")
def accounts_register():
    return render_template("accounts_new.html")


@app.route("/accounts/create", methods=["POST"])
def accounts_new():
    username, firstname, lastname, password1, password2 = request.form.values()
    new_index, messages = add_user(
        username=username,
        firstname=firstname,
        lastname=lastname,
        password1=password1,
        password2=password2,
    )
    [flash(message) for message in messages]
    if str(new_index).isnumeric and new_index > 0:
        return redirect(f"/accounts/{new_index}")
    return render_template(
        "accounts_new.html",
        form_data=request.form,
    )


@app.route("/accounts/login", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    ret = check_username_and_password(username, password)
    if not ret:
        flash("Error: Login failed.")
        return redirect(request.referrer or "/")
    session["user_id"], session["username"], session["screenname"] = ret
    flash("Success: Login was succesful.")
    return redirect(request.referrer or "/")


@app.route("/restaurants")
def restaurants():
    return render_template("restaurants_list.html", restaurants=get_restaurants_all())


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant(restaurant_id):
    restaurant = get_restaurants_single(restaurant_id)
    return render_template("restaurants_single.html", restaurant=restaurant)


@app.route("/restaurants/new")
def new_restaurant_page():
    return render_template("restaurants_new.html")


@app.route("/restaurants/create", methods=["POST"])
def new_restaurant():
    if not session["user_id"]:
        flash("Error: You are not logged in.")
        return redirect(request.referrer or "/restaurants/new")
    admin_id = session["user_id"]
    new_index, error = add_restaurant(
        admin_id=admin_id, name=request.form["name"], address=request.form["address"]
    )
    if error or not str(new_index).isnumeric or new_index < 1:
        [flash(f"Error: {err}") for err in error]
        return render_template("/restaurants/new")
    flash("Success: Restaurant created.")
    return redirect(f"/restaurants/{new_index}")


@app.route("/ratings")
def ratings():
    return render_template("ratings_list.html", ratings=get_ratings_all())


@app.route("/ratings/<int:rating_id>")
def single_rating(rating_id):
    rating = get_ratings_single(rating_id)
    return render_template("ratings_single.html", rating=rating)
