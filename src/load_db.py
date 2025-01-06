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
    ("molly", "millions", "molly", "millions"),
    ("case", "casecase", "henry", "case"),
    ("lupus", "lupuslupus", "lupus", "yonderboy"),
    ("deane", "deanedeane", "julius", "deane"),
    ("longhum", "longhum", "long", "hum"),
    ("danielle", "danielle", "danielle", "stark"),
    ("crowjane", "crowjane", "crow", "jane"),
    ("robin", "robinrobin", "robin", "lanier"),
    ("virginia", "virginia", "virginia", "rambaldi"),
]

sql = """INSERT INTO accounts (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)"""
[
    cur.execute(sql, (acc[0], generate_password_hash(acc[1]), acc[2], acc[3]))
    for acc in accounts
]
conn.commit()
# cur.executemany(sql, accounts)
restaurants = [
    ("le bar", 1, "Mannerheimintie 1", 60.1692, 24.9402, 123456789),
    ("le restaurant", 2, "Mannerheimintie 3", 60.1700, 24.9410, 987654321),
    ("le other restaurant", 3, "Korkeavuorenkatu 22", 60.1605, 24.9507, 234567890),
    ("good restaurant", 4, "Liisankatu 14", 60.1801, 24.9490, 345678901),
    ("bar f", 1, "Kaivokatu 3", 60.1715, 24.9415, 456789012),
    ("bar t", 2, "Simonkatu 4", 60.1680, 24.9310, 567890123),
    ("ristorant E", 3, "Kaivokatu 2", 60.1710, 24.9400, 678901234),
]
sql = """INSERT INTO restaurants (name, account_id, address, latitude, longitude, place_id) VALUES (%s, %s, %s, %s, %s, %s)"""
cur.executemany(sql, restaurants)
conn.commit()


events = [
    (
        "B-Day Bash",
        datetime(2025, 2, 1, 18, 0),
        datetime(2025, 2, 1, 23, 0),
        1,
        1,
        "Celebrate a birthday bash!",
    ),
    (
        "The Ritual",
        datetime(2025, 1, 30, 20, 0),
        datetime(2025, 1, 30, 23, 30),
        2,
        2,
        "A mysterious ritual event.",
    ),
    (
        "Tuomiopäivä - Keinäsen Nimipäivä",
        datetime(2025, 6, 6, 12, 0),
        datetime(2025, 6, 6, 15, 0),
        3,
        1,
        "A special name day celebration.",
    ),
    (
        "KrisKros Megaparty",
        datetime(2025, 4, 30, 21, 0),
        datetime(2025, 5, 1, 2, 0),
        1,
        4,
        "Get ready for a KrisKros mega event!",
    ),
    (
        "WappuLounas",
        datetime(2025, 5, 1, 11, 0),
        datetime(2025, 5, 1, 14, 0),
        4,
        4,
        "A traditional Wappu lunch.",
    ),
    (
        "Trivia Night",
        datetime(2025, 2, 14, 19, 0),
        datetime(2025, 2, 14, 21, 0),
        5,
        5,
        "Test your knowledge at trivia night.",
    ),
    (
        "Jazz Evening",
        datetime(2025, 3, 10, 18, 30),
        datetime(2025, 3, 10, 22, 0),
        6,
        6,
        "Enjoy live jazz performances.",
    ),
    (
        "Coding Marathon",
        datetime(2025, 4, 5, 9, 0),
        datetime(2025, 4, 5, 18, 0),
        7,
        7,
        "Collaborate and code all day.",
    ),
    (
        "Art Showcase",
        datetime(2025, 2, 20, 17, 0),
        datetime(2025, 2, 20, 20, 30),
        1,
        8,
        "Local artists showcase their work.",
    ),
    (
        "Open Mic Night",
        datetime(2025, 3, 25, 19, 0),
        datetime(2025, 3, 25, 22, 0),
        2,
        9,
        "Share your talent or watch others perform.",
    ),
    (
        "Wine Tasting",
        datetime(2025, 4, 18, 18, 0),
        datetime(2025, 4, 18, 21, 0),
        3,
        10,
        "Sample fine wines with friends.",
    ),
    (
        "Gaming Tournament",
        datetime(2025, 5, 12, 10, 0),
        datetime(2025, 5, 12, 18, 0),
        4,
        11,
        "Compete in a day-long gaming event.",
    ),
    (
        "Book Club Meetup",
        datetime(2025, 6, 7, 16, 0),
        datetime(2025, 6, 7, 18, 0),
        5,
        12,
        "Discuss the latest book with fellow readers.",
    ),
    (
        "Charity Gala",
        datetime(2025, 6, 20, 19, 0),
        datetime(2025, 6, 20, 23, 0),
        6,
        13,
        "Support a good cause at this elegant gala.",
    ),
    (
        "Summer Picnic",
        datetime(2025, 7, 15, 12, 0),
        datetime(2025, 7, 15, 16, 0),
        7,
        14,
        "Join us for a relaxing summer picnic.",
    ),
]


sql = """INSERT INTO events (active, name, start_time, end_time, restaurant_id, account_id, description) VALUES (TRUE, %s, %s, %s, %s, %s, %s)"""
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
