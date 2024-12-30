from datetime import date, timedelta
from db_module import (
    create_user,
    create_event,
    get_account_by_id,
    get_account_by_username,
    get_accountWithPassword_by_username,
    get_restaurants_all,
    get_restaurants_by_id,
)

from werkzeug.security import check_password_hash, generate_password_hash


def add_user(
    username: str, firstname: str, lastname: str, password1: str, password2: str
):

    error = []
    if password1 != password2:
        error.append("Error: Passwords did not match.")
    if not username or not 3 < len(username) < 25:
        error.append("Error: Username should be between 4-24 characters long")
    if get_account_by_username(username):
        error.append("Error: Username is use")
    if not 7 < len(password1) < 33:
        error.append("Error: password should be between 8-32 characters long")
    if (firstname and len(firstname) > 63) or (lastname and len(lastname) > 63):
        error.append("Error: Names can't be over 63 characters long")
    if not error:
        ret = create_user(
            username, firstname, lastname, generate_password_hash(password1)
        )
        if ret:
            return ret, ["Success: User created."]
        error.append("Error: There was an error creating user.")
    return -1, error


def add_event(name: str, restaurant_id_string: str, date_string: str, account_id: int):
    error = []
    if not name or len(name) > 64:
        error.append("Error: not a valid name. It should be 4-64 characters long")
    if not restaurant_id_string.isdigit:
        error.append("Error: that venue id is not recognized")
    restaurant_id = None
    try:
        restaurant_id = int(restaurant_id_string)
        if restaurant_id < 1 or not get_restaurants_by_id(restaurant_id):
            error.append("Error: that venue id is not recognized")
    except ValueError:
        error.append("Error: venue_id was not a valid number")
    event_date = None
    try:
        event_date = date.fromisoformat(date_string)
        if not event_date:
            error.append("Error: date was not in a valid format")
        if event_date < date.today():
            error.append("Error: past dates not accepted because: reasons")
        if event_date > date.today() + timedelta(days=3650):
            error.append("Error: date can't be more than 10 years from today")
    except ValueError:
        error.append("Error: date was not in a valid format")
    if not get_account_by_id(account_id):
        error.append("Error: events can only be announced by valid users")
    if not error and restaurant_id and event_date:
        ret = create_event(name, restaurant_id, event_date, account_id)
        if ret:
            return ret, error
    return -1, error


def check_username_and_password(username: str, password: str):
    user = get_accountWithPassword_by_username(username)
    print(f"{user=}")
    if not user:
        return None
    if check_password_hash(user.password, password):
        return (user.id, user.firstname or user.lastname or user.username)
    return None


def get_map_data():
    restaurants = get_restaurants_all()
    return [(r.id, r.name, r.latitude, r.longitude) for r in restaurants]
