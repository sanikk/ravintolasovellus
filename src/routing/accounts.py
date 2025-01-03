from flask import render_template, request, redirect, session, flash
from app import app

from db_module import (
    create_user,
    update_account_by_id,
    get_account_by_id,
    get_restaurants_by_accountId,
    get_events_by_accountId,
    get_ratings_by_accountId,
)
from service.validation_service import (
    validate_account_data,
    check_username_and_password,
)

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


@app.route("/accounts/edit/<int:account_id>")
def accounts_edit_form(account_id: int):
    account = get_account_by_id(account_id)
    if (
        not account_id
        or not account
        or not "user_id" in session
        or session["user_id"] != account_id
    ):
        flash("Error: You are not logged in as the owner of this account.")
        return redirect("/")
    return render_template("accounts_edit.html", account=account)


@app.route("/accounts/update/<int:account_id>", methods=["POST"])
def update_accounts_endpoint(account_id: int):
    if "user_id" in session and session["user_id"] == account_id:
        account = get_account_by_id(account_id)
        username = request.form["username"]
        if account:
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            newpassword1 = request.form["newpassword1"]
            newpassword2 = request.form["newpassword2"]
            oldpassword = request.form["oldpassword"]

            if check_username_and_password(account.username, oldpassword):
                password_hash = None
                error = None

                if newpassword1 and newpassword2:
                    password_hash, error = validate_account_data(
                        username, firstname, lastname, newpassword1, newpassword2
                    )
                else:
                    _, error = validate_account_data(
                        username, firstname, lastname, oldpassword, oldpassword
                    )

                if not error:
                    ret = update_account_by_id(
                        account_id, username, firstname, lastname, password_hash
                    )
                    if ret:
                        return redirect(f"/accounts/{account_id}")
                    error.append(
                        "Error: something went wrong trying to update your account."
                    )
                [flash(err) for err in error]
                return redirect("/")

    flash("Error: Credentials don't match the owner of this account.")
    return redirect("/")


####################################
# LOGIN/LOGOUT/REGISTRATION        #
####################################


@app.route("/accounts/registration")
def accounts_register():
    return render_template("accounts_new.html")


@app.route("/accounts/create", methods=["POST"])
def accounts_new():
    username, firstname, lastname, password1, password2 = request.form.values()
    password_hash, error = validate_account_data(
        username=username,
        firstname=firstname,
        lastname=lastname,
        password1=password1,
        password2=password2,
    )
    if not error and password_hash:
        return_value = create_user(username, firstname, lastname, password_hash)
        if return_value:
            session["user_id"] = return_value
            session["screenname"] = firstname or lastname or username
            return redirect(f"/accounts/{return_value}")
        error.append(
            "Error: Something went wrong creating the account. No return value."
        )
    [flash(err) for err in error]
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
