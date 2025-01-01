from db_module import get_account_by_id
from service.convert_address import get_lat_long_placeid


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
    lat, long, place_id = get_lat_long_placeid(address + " Helsinki")
    if not lat or not long or not place_id:
        error.append("Error: There was an error resolving the address.")
    return lat, long, place_id, error
