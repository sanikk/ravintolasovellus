from flask import render_template, request, redirect, session, flash
from app import app

from db_module import (
    get_accounts_all,
    get_account_by_user_id,
    get_restaurants_by_admin_id,
    get_events_by_account_id,
    get_ratings_by_account_id,
)
from service.helper_service import add_user, check_username_and_password

#################################
# ACCOUNTS                      #
#################################


@app.route("/accounts")
def accounts():
    accounts_list = get_accounts_all()
    return render_template("accounts_list.html", accounts=accounts_list)


@app.route("/accounts/<int:user_id>")
def accounts_single(user_id: int):
    account = get_account_by_user_id(user_id)
    restaurants = get_restaurants_by_admin_id(user_id)
    events = get_events_by_account_id(user_id)
    ratings = get_ratings_by_account_id(user_id)
    return render_template(
        "accounts_single.html",
        account=account,
        restaurants=restaurants,
        events=events,
        ratings=ratings,
    )


####################################
# LOGIN/LOGOUT/REGISTRATION        #
####################################


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
    session["user_id"], session["screenname"] = ret
    flash("Success: Login was succesful.")
    return redirect(request.referrer or "/")


@app.route("/accounts/logout")
def logout_user():
    del session["user_id"]
    del session["screenname"]
    return redirect(request.referrer or "/")
