from flask import render_template, request, redirect, session, flash
from app import app

from db_module import (
    get_account_by_id,
    get_restaurants_by_accountId,
    get_events_by_accountId,
    get_ratings_by_accountId,
)
from service.helper_service import add_user, check_username_and_password

#################################
# ACCOUNTS                      #
#################################

# Yeah not setting up real access control for admin account here. We can use psql.

# @app.route("/accounts")
# def accounts():
#     accounts_list = get_accounts_all()
#     return render_template("accounts_list.html", accounts=accounts_list)


@app.route("/accounts/<int:account_id>")
def accounts_single(account_id: int):
    if session["user_id"] != account_id:
        flash("Error: You are not logged in as the owner of this account.")
        return redirect("/")
    account = get_account_by_id(account_id)
    restaurants = get_restaurants_by_accountId(account_id)
    events = get_events_by_accountId(account_id)
    ratings = get_ratings_by_accountId(account_id)
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
        session["user_id"] = new_index
        session["screenname"] = firstname or lastname or username
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
    session.clear()
    return redirect(request.referrer or "/")
