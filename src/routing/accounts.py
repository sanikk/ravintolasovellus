from flask import render_template, request, redirect, session, flash
from app import app

from db_module import (
    create_user,
    get_events_list_by_accountId,
    update_account_by_id,
    get_account_by_id,
    get_restaurants_by_accountId,
    get_ratings_by_accountId,
)
from service.validation_service import (
    validate_account_data,
    check_username_and_password,
)

#################################
# ACCOUNTS                      #
#################################


@app.route("/accounts/<int:account_id>")
def accounts_single(account_id: int):
    if "user_id" not in session or session["user_id"] != account_id:
        flash("Error: You are not logged in as the owner of this account.")
        return redirect("/")
    account = get_account_by_id(account_id)
    restaurants = get_restaurants_by_accountId(account_id)
    events = get_events_list_by_accountId(account_id)
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
    if account_id:
        account = get_account_by_id(account_id)
        if account and "user_id" in session and session["user_id"] == account_id:
            return render_template("accounts_edit.html", account=account, form_data={})
    flash("Error: You are not logged in as the owner of this account.")
    return redirect("/")


@app.route("/accounts/update/<int:account_id>", methods=["POST"])
def update_accounts_endpoint(account_id: int):
    if "user_id" in session and session["user_id"] == account_id:
        account = get_account_by_id(account_id)
        if account:
            user_info = {
                "username": request.form["username"],
                "email": request.form["email"],
                "billing_info": request.form["billing_info"],
                "firstname": request.form["firstname"],
                "lastname": request.form["lastname"],
                "description": request.form["description"],
            }
            newpassword1 = request.form["newpassword1"]
            newpassword2 = request.form["newpassword2"]
            oldpassword = request.form["oldpassword"]

            if check_username_and_password(account.username, oldpassword):
                password_hash, error = validate_account_data(
                    **user_info,
                    password1=newpassword1,
                    password2=newpassword2,
                )

                if not error:
                    ret = update_account_by_id(
                        account_id=account_id,
                        **user_info,
                        password_hash=password_hash,
                    )
                    if ret:
                        return redirect(f"/accounts/{account_id}")
                    error.append(
                        "Error: something went wrong trying to update your account."
                    )
                [flash(err) for err in error]
                return render_template(
                    "accounts_edit.html", account=account, form_data=request.form
                )

    flash("Error: Credentials don't match the owner of this account.")
    return redirect("/")


####################################
# LOGIN/LOGOUT/REGISTRATION        #
####################################


@app.route("/accounts/registration")
def accounts_register():
    return render_template("accounts_new.html", form_data={})


@app.route("/accounts/create", methods=["POST"])
def accounts_new():
    user_info = {
        "username": request.form["username"],
        "email": request.form["email"],
        "billing_info": request.form["billing_info"],
        "firstname": request.form["firstname"],
        "lastname": request.form["lastname"],
        "description": request.form["description"],
    }
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not password1 or not password2 or password1 != password2:
        flash("Error: please enter the same password in both password fields")
    elif not (user_info["firstname"] or user_info["lastname"]):
        flash(
            "Error: You should give some kind of first name or last name we can show."
        )

    else:

        password_hash, error = validate_account_data(
            **user_info,
            password1=password1,
            password2=password2,
        )
        if not error and password_hash:
            return_value = create_user(
                **user_info,
                password_hash=password_hash,
            )
            if return_value:
                session["user_id"] = return_value
                session["screenname"] = (
                    user_info["firstname"]
                    or user_info["lastname"]
                    or user_info["username"]
                )
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
    return redirect(request.referrer or f"/accounts/{ret}")


@app.route("/accounts/logout")
def logout_user():
    session.clear()
    return redirect(request.referrer or "/")
