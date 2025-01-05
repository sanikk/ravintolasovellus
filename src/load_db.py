from psycopg import connect
from service.convert_address import get_lat_long_placeid
from werkzeug.security import generate_password_hash
from config import DATABASE_NAME
from datetime import date, datetime


def get_connection():
    conn = connect(f"dbname={DATABASE_NAME}")
    print(f"Connected to {DATABASE_NAME}")
    cur = conn.cursor()
    return conn, cur


conn, cur = get_connection()

accounts = [
    ("jekku", "jekkujekku", "", "Vesuri"),
    ("esko", "eskoesko", "esko", "mörkö"),
    ("tauno", "taunotauno", "tauno", "tanhuvainen"),
    ("pekka", "pekkapekka", "pekka", "piupelipoo"),
    ("camacho", "camacho", "mountain dew", "camacho"),
]
sql = """INSERT INTO accounts (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)"""
cur.executemany(sql, accounts)
restaurants = [
    ("le bar", 1, "Mannerheimintie 1", 60.1692, 24.9402, 123456789),
    ("le restaurant", 2, "Mannerheimintie 3", 60.1700, 24.9410, 987654321),
    ("le other restaurant", 3, "Korkeavuorenkatu 22", 60.1605, 24.9507, 234567890),
    ("good restaurant", 4, "Liisankatu 14", 60.1801, 24.9490, 345678901),
    ("bar f", 1, "Kaivokatu 3", 60.1715, 24.9415, 456789012),
    ("bar t", 2, "Simonkatu 4", 60.1680, 24.9310, 567890123),
    ("ristorant E", 3, "Kaivokatu 2", 60.1710, 24.9400, 678901234),
]
# restaurants = [
#     ("le bar", 1, "Mannerheimintie 1"),
#     ("le restaurant", 2, "Mannerheimintie 3"),
#     ("le other restaurant", 3, "Korkeavuorenkatu 22"),
#     ("good restaurant", 4, "Liisankatu 14"),
#     ("bar f", 1, "Kaivokatu 3"),
#     ("bar t", 2, "Simonkatu 4"),
#     ("ristorant E", 3, "Kaivokatu 2"),
# ]
sql = """INSERT INTO restaurants (name, account_id, address, latitude, longitude, place_id) VALUES (%s, %s, %s, %s, %s, %s)"""
cur.executemany(sql, restaurants)
conn.commit()


events = [
    ("B-Day Bash", date(2025, 2, 1), 1, 1),
    ("The Ritual", date(2025, 1, 30), 2, 2),
    ("Tuomiopäivä - Keinäsen Nimipäivä", date(2025, 6, 6), 3, 1),
    ("KrisKros Megaparty", date(2025, 4, 30), 1, 4),
    ("WappuLounas", date(2025, 5, 1), 4, 4),
]


sql = """INSERT INTO events (active, name, event_date, restaurant_id, account_id) VALUES (%s, TRUE, %s, %s, %s)"""
cur.executemany(sql, events)

ratings = [
    (2, 1, 5, "Great service, loved the food!"),
    (3, 1, 4, "Nice ambiance but could improve."),
    (4, 2, 3, "Delicious dishes, will visit again!"),
    (5, 2, 4, "Good but overpriced drinks."),
    (1, 3, 5, "Amazing flavors and fast service!"),
    (4, 3, 4, "Cozy place, enjoyed the experience."),
    (5, 4, 5, "Excellent menu, very satisfying!"),
    (2, 5, 3, "Decent food but slow service."),
    (3, 6, 4, "Friendly staff, will return soon!"),
]
sql = """INSERT INTO ratings (account_id, restaurant_id, rating, content) VALUES (%s, %s, %s, %s)"""
cur.executemany(sql, ratings)
conn.commit()
