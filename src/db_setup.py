from psycopg import connect
from psycopg.sql import SQL, Identifier
from src.config import DATABASE_NAME

# from werkzeug.security import generate_password_hash


def get_connection():
    conn = connect(f"dbname={DATABASE_NAME}")
    print(f"Connected to {DATABASE_NAME}")
    cur = conn.cursor()
    return conn, cur


def drop_tables():
    conn, cur = get_connection()
    table_list = [
        "events",
        "buffets",
        "ratings",
        "opening_hours",
        "restaurants",
        "messages",
        "accounts",
    ]
    for table in table_list:
        sql = SQL("DROP TABLE IF EXISTS {}").format(Identifier(table))
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Database had been cleaned.")


def create_tables():
    conn, cur = get_connection()
    # sql = SQL("ALTER DATABASE {} SET datestyle TO 'ISO, DMY'").format(
    #     Identifier(DATABASE_NAME)
    # )
    # cur.execute(sql)
    # conn.commit()

    # id, active, username, password, email, billing_info, firstname, lastname, description
    sql = """CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        username VARCHAR(32) UNIQUE,
        password VARCHAR(256),
        email VARCHAR(64),
        billing_info VARCHAR(256),
        firstname VARCHAR(32),
        lastname VARCHAR(32),
        description VARCHAR(500)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        name VARCHAR(64),
        account_id INTEGER REFERENCES accounts(id),
        latitude FLOAT,
        longitude FLOAT,
        place_id VARCHAR(20),
        address VARCHAR(128),
        description VARCHAR(500)
    )"""
    cur.execute(sql)
    sql = """CREATE INDEX idx_account_active ON restaurants (account_id, active);"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        account_id INTEGER REFERENCES accounts(id),
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        content VARCHAR(500)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT FALSE,
        name VARCHAR(128),
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        account_id INTEGER REFERENCES accounts(id),
        start_time TIMESTAMPTZ,
        end_time TIMESTAMPTZ,
        description VARCHAR(500)
    )"""
    cur.execute(sql)
    # event_date DATE,

    sql = """CREATE TABLE IF NOT EXISTS buffets (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        restaurant_id INTEGER REFERENCES restaurants(id),
        name VARCHAR(128),
        monday BOOL,
        tuesday BOOL,
        wednesday BOOL,
        thursday BOOL,
        friday BOOL,
        saturday BOOL,
        sunday BOOL,
        starttime TIME,
        endtime TIME,
        description VARCHAR(500)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        sender_id INTEGER REFERENCES accounts(id),
        receiver_id INTEGER REFERENCES accounts(id),
        sent_on TIMESTAMPTZ DEFAULT NOW(),
        title VARCHAR(256),
        content VARCHAR(2048)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS opening_hours (
        restaurant_id INTEGER REFERENCES restaurants(id),
        day_id INTEGER CHECK(day_id BETWEEN 1 and 7),
        opens_at TIME,
        closes_at TIME,
        PRIMARY KEY(restaurant_id, day_id)
    )"""
    cur.execute(sql)

    #     sql = """CREATE TABLE IF NOT EXISTS specialities (
    #         id SERIAL PRIMARY KEY,
    #         name TEXT
    #     )"""
    #     cur.execute(sql)
    #
    #     sql = """CREATE TABLE IF NOT EXISTS speciality_restaurants (
    #         restaurant_id INTEGER REFERENCES restaurants(id),
    #         speciality_id INTEGER REFERENCES specialities(id)
    #     )"""
    #     cur.execute(sql)

    #     ADMIN_USERNAME = input("Please enter an admin username: ")
    #     ADMIN_PASSWORD = input("Please enter an admin password: ")
    #     if (
    #         ADMIN_USERNAME
    #         and ADMIN_PASSWORD
    #         and 4 < len(ADMIN_USERNAME) < 17
    #         and 4 < len(ADMIN_PASSWORD) < 33
    #     ):
    #         cur.execute(
    #             """INSERT INTO account (username, password) VALUES (%s, %s)""",
    #             (ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD)),
    #         )
    print("Database has been built")
    conn.commit()
    cur.close()
    conn.close()
