import requests


def get_lat_long_placeid(street_address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": street_address,
        "format": "json",
        "addressdetails": 1,
        "class": "place",
    }
    headers = {"User-Agent": "MyRestaurantApp/1.0 (sanikk@users.noreply.github.com)"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(response.text)
        exit()
    data = response.json()
    if data:
        print(data)
        return float(data[0]["lat"]), float(data[0]["lon"]), int(data[0]["place_id"])
    return None, None, None
