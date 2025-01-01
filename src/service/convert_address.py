from requests import get
from flask import flash


def get_lat_long_placeid(street_address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": street_address,
        "format": "json",
        "addressdetails": 1,
        "class": "place",
    }
    headers = {"User-Agent": "MyRestaurantApp/1.0 (sanikk@users.noreply.github.com)"}
    response = get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error using openstreetmap api, status code {response.status_code}")
        print(response.text)
        flash(
            f"Error: there was an error using openstreetmap api, status code {response.status_code}"
        )
        return None, None, None
    data = response.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"]), int(data[0]["place_id"])
    return None, None, None
