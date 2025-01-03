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

users = [
    ("jekku", "pooppoop", "Vesuri"),
    ("esko", "eskoesko", "mörkö"),
    ("tauno", "taunotauno", "tanhuvainen"),
    ("pekka", "pekkapekka", "piupelipoo"),
]
sql = """INSERT INTO accounts (username, password, lastname) VALUES (%s, %s, %s)"""
for username, password, lastname in users:
    cur.execute(
        sql,
        (username, generate_password_hash(password), lastname),
    )
conn.commit()

restaurants = [
    ("le bar", 1, "Mannerheimintie 1"),
    ("le restaurant", 2, "Mannerheimintie 3"),
    ("le other restaurant", 3, "Korkeavuorenkatu 22"),
    ("good restaurant", 4, "Liisankatu 14"),
    ("bar f", 1, "Kaivokatu 3"),
    ("bar t", 2, "Simonkatu 4"),
    ("ristorant E", 3, "Kaivokatu 2"),
]
sql = """INSERT INTO restaurants (name, account_id, address, latitude, longitude, place_id) VALUES (%s, %s, %s, %s, %s, %s)"""
for name, account_id, address in restaurants:
    print(f"{name=}")
    lat, long, place_id = get_lat_long_placeid(address)
    print(f"{lat=}, {long=}, {place_id=}")
    cur.execute(
        sql,
        (name, account_id, address, lat, long, place_id),
    )
conn.commit()


events = [
    ("B-Day Bash", date(2025, 2, 1), 1, 1),
    ("The Ritual", date(2025, 1, 30), 2, 2),
    ("Tuomiopäivä - Keinäsen Nimipäivä", date(2025, 6, 6), 3, 1),
    ("KrisKros Megaparty", date(2025, 4, 30), 1, 4),
    ("WappuLounas", date(2025, 5, 1), 4, 4),
]


sql = """INSERT INTO events (name, event_date, restaurant_id, posted_on, account_id) VALUES (%s, %s, %s, NOW(), %s)"""
for name, event_date, restaurant_id, account_id in events:
    cur.execute(
        sql,
        (name, event_date, restaurant_id, account_id),
    )
conn.commit()
