import sqlite3
from werkzeug.security import generate_password_hash


def fill_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

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
    sql = """INSERT INTO accounts (username, password, firstname, lastname) VALUES (?, ?, ?, ?)"""
    cur.executemany(
        sql,
        [(acc[0], generate_password_hash(acc[1]), acc[2], acc[3]) for acc in accounts],
    )
    conn.commit()

    restaurants = [
        ("le bar", 1, "Mannerheimintie 1", 60.1692, 24.9402, 123456789),
        ("le restaurant", 2, "Mannerheimintie 3", 60.1700, 24.9410, 987654321),
        ("le other restaurant", 3, "Korkeavuorenkatu 22", 60.1605, 24.9507, 234567890),
        ("good restaurant", 4, "Liisankatu 14", 60.1801, 24.9490, 345678901),
        ("bar f", 1, "Kaivokatu 3", 60.1715, 24.9415, 456789012),
        ("bar t", 2, "Simonkatu 4", 60.1680, 24.9310, 567890123),
        ("ristorant E", 3, "Kaivokatu 2", 60.1710, 24.9400, 678901234),
    ]
    sql = """INSERT INTO restaurants (name, account_id, address, latitude, longitude, place_id) VALUES (?, ?, ?, ?, ?, ?)"""
    cur.executemany(sql, restaurants)
    conn.commit()

    events = [
        (
            "B-Day Bash",
            "2025-02-01 18:00:00",
            "2025-02-01 23:00:00",
            1,
            1,
            "Celebrate a birthday bash!",
        ),
        (
            "The Ritual",
            "2025-01-30 20:00:00",
            "2025-01-30 23:30:00",
            2,
            2,
            "A mysterious ritual event.",
        ),
        (
            "Tuomiopäivä - Keinäsen Nimipäivä",
            "2025-06-06 12:00:00",
            "2025-06-06 15:00:00",
            3,
            1,
            "A special name day celebration.",
        ),
        (
            "KrisKros Megaparty",
            "2025-04-30 21:00:00",
            "2025-05-01 02:00:00",
            1,
            4,
            "Get ready for a KrisKros mega event!",
        ),
        (
            "WappuLounas",
            "2025-05-01 11:00:00",
            "2025-05-01 14:00:00",
            4,
            4,
            "A traditional Wappu lunch.",
        ),
        (
            "Trivia Night",
            "2025-02-14 19:00:00",
            "2025-02-14 21:00:00",
            5,
            5,
            "Test your knowledge at trivia night.",
        ),
        (
            "Jazz Evening",
            "2025-03-10 18:30:00",
            "2025-03-10 22:00:00",
            6,
            6,
            "Enjoy live jazz performances.",
        ),
        (
            "Coding Marathon",
            "2025-04-05 09:00:00",
            "2025-04-05 18:00:00",
            7,
            7,
            "Collaborate and code all day.",
        ),
        (
            "Art Showcase",
            "2025-02-20 17:00:00",
            "2025-02-20 20:30:00",
            1,
            8,
            "Local artists showcase their work.",
        ),
        (
            "Open Mic Night",
            "2025-03-25 19:00:00",
            "2025-03-25 22:00:00",
            2,
            9,
            "Share your talent or watch others perform.",
        ),
        (
            "Wine Tasting",
            "2025-04-18 18:00:00",
            "2025-04-18 21:00:00",
            3,
            10,
            "Sample fine wines with friends.",
        ),
        (
            "Gaming Tournament",
            "2025-05-12 10:00:00",
            "2025-05-12 18:00:00",
            4,
            11,
            "Compete in a day-long gaming event.",
        ),
        (
            "Book Club Meetup",
            "2025-06-07 16:00:00",
            "2025-06-07 18:00:00",
            5,
            12,
            "Discuss the latest book with fellow readers.",
        ),
        (
            "Charity Gala",
            "2025-06-20 19:00:00",
            "2025-06-20 23:00:00",
            6,
            13,
            "Support a good cause at this elegant gala.",
        ),
        (
            "Summer Picnic",
            "2025-07-15 12:00:00",
            "2025-07-15 16:00:00",
            7,
            14,
            "Join us for a relaxing summer picnic.",
        ),
    ]
    sql = """INSERT INTO events (active, name, start_time, end_time, restaurant_id, account_id, description) VALUES (1, ?, ?, ?, ?, ?, ?)"""
    cur.executemany(sql, events)
    conn.commit()

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
    sql = """INSERT INTO ratings (account_id, restaurant_id, rating, content) VALUES (?, ?, ?, ?)"""
    cur.executemany(sql, ratings)
    conn.commit()

    cur.close()
    conn.close()
    print("Database filled successfully!")
