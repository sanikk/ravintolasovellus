from datetime import date, timedelta
from db_module import (
    create_event,
    get_account_by_id,
    get_restaurants_by_id,
)


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
