from datetime import time

from db_module import (
    get_account_by_id,
    get_account_by_username,
    check_account_email,
    get_accountId_by_restaurantId,
    get_restaurants_by_id,
)
from service.convert_address import get_lat_long_placeid
from werkzeug.security import check_password_hash, generate_password_hash
import re


def validate_restaurant_data(
    name: str, account_id: int, address: str, description: str
):
    error = []
    if (
        not account_id
        or not account_id.is_integer()
        or account_id < 1
        or not get_account_by_id(account_id)
    ):
        error.append("Error: Invalid account_id.")
    if not name or not 0 < len(name) < 65:
        error.append("Error: Restaurant needs a name with 1-64 characters.")
    if not address or not 3 < len(address) < 65:
        error.append("Error: Restaurant needs an address, with 4-64 characters.")
    lat, long, place_id = get_lat_long_placeid(address)
    if not lat or not long or not place_id:
        error.append("Error: There was an error resolving the address.")
    if description and not 2 < len(description) < 501:
        error.append("Error: The description does not seem valid")
    return lat, long, place_id, error


def validate_account_data(
    username: str,
    email: str,
    billing_info: str,
    firstname: str,
    lastname: str,
    description: str,
    password1: str,
    password2: str,
):
    error = []
    password_hash = ""
    if password1 != password2:
        error.append("Error: Passwords did not match.")
    if password1 and not 7 < len(password1) < 33:
        error.append("Error: password should be between 8-32 characters long")
    if password1 and not error:
        password_hash = generate_password_hash(password1)
        if not password_hash:
            error.append("Error: something went wrong hashing your password.")

    if username:
        if not 3 < len(username) < 33:
            error.append("Error: Username should be between 4-24 characters long")
        if get_account_by_username(username):
            error.append("Error: Username is in use")

    if email:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            error.append("Error: that does not seem like a valid email address")
        if len(email) > 64:
            error.append("Error: that email is over 64 characters long")
        if check_account_email(email):
            error.append("Error: that email is already in use.")

    if billing_info:
        if not 5 < len(billing_info) < 257:
            error.append(
                "Error: billing info should be valid and consist of 6-256 characters"
            )
    if (firstname and len(firstname) > 32) or (lastname and len(lastname) > 32):
        error.append("Error: Names can't be over 32 characters long")
    if description and len(description) > 500:
        error.append(
            "Error: Your tagline can't be over 500 characters. Please condense it."
        )
    return password_hash, error


def validate_buffet_data(user_input: dict):
    error = []
    if not "name" in user_input or not 3 < len(user_input["name"]) < 65:
        error.append("Error: Name needs to be 4-64 characters long")

    if not "account_id" in user_input or not get_account_by_id(
        user_input["account_id"]
    ):
        error.append("Error: You should be logged in with a valid user account")

    if "restaurant_id" in user_input:
        ret = get_accountId_by_restaurantId(user_input["restaurant_id"])
        if not ret or ret != user_input["account_id"]:
            error.append("Error: Please choose a restaurant you are admin of")
    else:
        error.append("Error: Please choose a restaurant you are admin of")

    if (
        not "days" in user_input
        or not user_input["days"]
        or not 0 < len(user_input["days"]) < 8
    ):
        error.append("Error: Please choose at least one day")

    if not "start_time" in user_input or not time(0, 0, 0) < user_input[
        "start_time"
    ] < time(24, 0, 0):
        error.append("Error: Please choose a valid starting time")

    if not "end_time" in user_input or not time(0, 0, 0) < user_input[
        "end_time"
    ] < time(24, 0, 0):
        error.append("Error: Please choose a valid ending time")

    if not "price" in user_input or not 0 < int(user_input["price"]):
        error.append("Error: Please choose a valid price")

    if not "description" in user_input or 2 < len(user_input["description"]) < 501:
        error.append("Error: Description should be between 3-500 characters long")

    return error


def check_username_and_password(username: str, password: str):
    if username and password:
        user = get_account_by_username(username)
        if user and check_password_hash(user.password, password):
            return (user.id, user.firstname or user.lastname or user.username)
    return None
