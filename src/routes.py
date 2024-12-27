from flask import flash, redirect, render_template, request, session, url_for
from app import app

# from convert_address import get_lat_long_placeid

from db_module import (
    create_restaurant,
    get_restaurants_all,
    get_restaurants_single,
)
from db_module import (
    get_accounts_all,
    check_username_and_password,
    get_account_by_user_id,
    get_account_by_username,
    create_user,
)
from db_module import get_ratings_all, get_ratings_single

from map_service import get_map


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
    error = []

    if password1 != password2:
        error.append("Passwords did not match.")
    if not username:
        error.append("Username can't be empty")
    if get_account_by_username(username):
        error.append("Username is use")
    if not error:
        create_user(username, firstname, lastname, password1)
        flash("User created.")
        return redirect(request.referrer or "/")

    return render_template(
        "accounts_new.html",
        form_data=request.form,
        error=error,
    )


@app.route("/accounts/login", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    ret = check_username_and_password(username, password)
    if not ret:
        return redirect(request.referrer or "/")
    # print(f"{ret=}")
    # session["user_id"] = ret.user_id
    session["user_id"], session["username"], session["screenname"] = ret
    return redirect(request.referrer or "/")


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


@app.route("/restaurants/create", methods=["POST"])
def new_restaurant():
    error = []
    if not session["user_id"]:
        error.append("You are not logged in.")
        return redirect(request.referrer or "/restaurants")
    admin_id = session["user_id"]
    name = request.form["name"]
    if not name:
        error.append("Restaurant needs a name.")
    address = request.form["address"]
    if not address:
        error.append("Restaurant needs an address.")
    # lat, long, place_id = get_lat_long_placeid(address)
    # if not lat or long:
    #     error.append("There was an error resolving the address.")
    ret = create_restaurant(name=name, admin_id=admin_id, address=address)
    if not ret:
        error.append("There was no return index. Something went wrong?")
    if error:
        return render_template("/restaurants/new", error=error)
    return redirect(request.referrer or "/restaurants")


@app.route("/ratings")
def ratings():
    return render_template("ratings_list.html", ratings=get_ratings_all())


@app.route("/ratings/<int:rating_id>")
def single_rating(rating_id):
    rating = get_ratings_single(rating_id)
    return render_template("ratings_single.html", rating=rating)
