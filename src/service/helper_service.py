from db_module import create_restaurant, create_user, get_account_by_username
from service.convert_address import get_lat_long_placeid


def add_restaurant(admin_id: int, name: str, address: str):
    error = []
    if not admin_id or not admin_id.is_integer() or admin_id < 1:
        error.append("Invalid user_id.")
    if not name:
        error.append("Restaurant needs a name.")
    if not address:
        error.append("Restaurant needs an address.")
    lat, long, place_id = get_lat_long_placeid(address)
    if not lat or not long or not place_id:
        error.append("There was an error resolving the address.")
    if not error:
        ret = create_restaurant(
            name=name,
            admin_id=admin_id,
            address=address,
            lat=lat,
            long=long,
            place_id=place_id,
        )
        if ret:
            return ret, error
        error.append("There was no return index. Something went wrong?")
    return -1, error


def add_user(
    username: str, firstname: str, lastname: str, password1: str, password2: str
):

    errors = []
    if password1 != password2:
        errors.append("Error: Passwords did not match.")
    if not username:
        errors.append("Error: Username can't be empty")
    if get_account_by_username(username):
        errors.append("Error: Username is use")
    if not errors:
        ret = create_user(username, firstname, lastname, password1)
        if ret:
            return ret, ["Success: User created."]
        errors.append("Error: There was an error creating user.")
    return -1, errors
