from psycopg import connect
from os import getenv
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    conn = connect(f"dbname={getenv('SQLALCHEMY_DATABASE_URI')}")
    cur = conn.cursor()
    return conn, cur


def drop_tables():
    conn, cur = get_connection()
    table_list = [
        "specialty_restaurant",
        "specialty",
        "event_date",
        "event",
        "buffet",
        "review",
        "restaurant",
        "account"
    ]
    for table in table_list:
        sql = f"DROP TABLE IF EXISTS {table}"
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def create_tables():
    conn, cur = get_connection()

    sql = """CREATE TABLE IF NOT EXISTS account (
        id SERIAL PRIMARY KEY,
        username TEXT,
        realname TEXT,
        password TEXT,
        role INTEGER
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS restaurant (
        id SERIAL PRIMARY KEY,
        name TEXT,
        latitude FLOAT,
        longitude FLOAT,
        place_id TEXT,
        address TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS review (
        id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES account(id),
        restaurant_id INTEGER REFERENCES restaurant(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        rating INTEGER,
        content TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS event (
        id SERIAL PRIMARY KEY,
        name TEXT,
        restaurant_id INTEGER REFERENCES restaurant(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        account_id INTEGER REFERENCES account(id)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS buffet (
        id SERIAL PRIMARY KEY,
        restaurant_id INTEGER REFERENCES restaurant(id)
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS event_date (
        id SERIAL PRIMARY KEY,
        event_id INTEGER REFERENCES event(id),
        event_date TIMESTAMPTZ
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS specialty (
        id SERIAL PRIMARY KEY,
        name TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS specialty_restaurant (
        restaurant_id INTEGER REFERENCES restaurant(id),
        specialty_id INTEGER REFERENCES specialty(id)
    )"""
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
