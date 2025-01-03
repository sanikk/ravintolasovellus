from db_module import (
    get_account_by_id,
    get_account_by_username,
    get_accountWithPassword_by_username,
)
from service.convert_address import get_lat_long_placeid
from werkzeug.security import check_password_hash, generate_password_hash


def validate_restaurant_data(name: str, account_id: int, address: str):
    error = []
    if (
        not account_id
        or not account_id.is_integer()
        or account_id < 1
        or not get_account_by_id(account_id)
    ):
        error.append("Error: Invalid account_id.")
    if not name or not 3 < len(name) < 65:
        error.append("Error: Restaurant needs a name with 4-64 characters.")
    if not address or not 3 < len(address) < 65:
        error.append("Error: Restaurant needs an address, with 4-64 characters.")
    lat, long, place_id = get_lat_long_placeid(address)
    if not lat or not long or not place_id:
        error.append("Error: There was an error resolving the address.")
    return lat, long, place_id, error


def validate_account_data(
    username: str, firstname: str, lastname: str, password1: str, password2: str
):
    error = []
    password_hash = ""
    if password1 != password2:
        error.append("Error: Passwords did not match.")
    if not 7 < len(password1) < 33:
        error.append("Error: password should be between 8-32 characters long")
    if not error:
        password_hash = generate_password_hash(password1)
        if not password_hash:
            error.append("Error: something went wrong hashing your password.")
    if not username or not 3 < len(username) < 25:
        error.append("Error: Username should be between 4-24 characters long")
    if get_account_by_username(username):
        error.append("Error: Username is use")
    if (firstname and len(firstname) > 63) or (lastname and len(lastname) > 63):
        error.append("Error: Names can't be over 63 characters long")
    return password_hash, error


def check_username_and_password(username: str, password: str):
    user = get_accountWithPassword_by_username(username)
    if not user:
        return None
    if check_password_hash(user.password, password):
        return (user.id, user.firstname or user.lastname or user.username)
    return None
