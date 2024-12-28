from psycopg import connect
from psycopg.sql import SQL, Identifier
from src.config import DATABASE_NAME


def get_connection():
    print(f"{DATABASE_NAME=}")
    conn = connect(f"dbname={DATABASE_NAME}")
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
        # sql = """DROP TABLE IF EXISTS %s"""
        sql = SQL("DROP TABLE IF EXISTS {}").format(Identifier(table))
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def create_tables():
    conn, cur = get_connection()

    sql = """CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        firstname TEXT,
        lastname TEXT,
        password TEXT,
        role INTEGER
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        name TEXT,
        admin_id INTEGER REFERENCES accounts(id),
        latitude FLOAT,
        longitude FLOAT,
        place_id TEXT,
        address TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES accounts(id),
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        rating INTEGER,
        content TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        name TEXT,
        event_date DATE,
        restaurant_id INTEGER REFERENCES restaurants(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        account_id INTEGER REFERENCES accounts(id)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS buffets (
        id SERIAL PRIMARY KEY,
        restaurant_id INTEGER REFERENCES restaurants(id)
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

    conn.commit()
    cur.close()
    conn.close()
