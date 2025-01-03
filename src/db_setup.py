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
        "speciality_restaurants",
        "specialities",
        "events",
        "buffets",
        "ratings",
        "restaurants",
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

    sql = """CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        active BOOL,
        username TEXT UNIQUE,
        firstname TEXT,
        lastname TEXT,
        password TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        active BOOL,
        name TEXT,
        account_id INTEGER REFERENCES accounts(id),
        latitude FLOAT,
        longitude FLOAT,
        place_id TEXT,
        address TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        active BOOL,
        account_id INTEGER REFERENCES accounts(id),
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        rating INTEGER,
        content TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        active BOOL,
        name TEXT,
        event_date DATE,
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        account_id INTEGER REFERENCES accounts(id)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS buffets (
        id SERIAL PRIMARY KEY,
        active BOOL,
        restaurant_id INTEGER REFERENCES restaurants(id),
        name TEXT,
        monday BOOL,
        tuesday BOOL,
        wednesday BOOL,
        thursday BOOL,
        friday BOOL,
        saturday BOOL,
        sunday BOOL,
        starttime TIME,
        endtime TIME
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS specialities (
        id SERIAL PRIMARY KEY,
        name TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS speciality_restaurants (
        restaurant_id INTEGER REFERENCES restaurants(id),
        speciality_id INTEGER REFERENCES specialities(id)
    )"""
    cur.execute(sql)

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
