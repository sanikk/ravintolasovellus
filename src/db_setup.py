from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    conn = connect(f"dbname={getenv('SQLALCHEMY_DATABASE_URI')}")
    cur = conn.cursor()
    return conn, cur


def drop_tables():
    conn, cur = get_connection()
    sql = "DROP TABLE IF EXISTS event_date"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS event"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS buffet"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS account"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS review"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS restaurant"
    cur.execute(sql)
    sql = "DROP TABLE IF EXISTS account"
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
        location TEXT,
        homepage TEXT,
        specialty TEXT,
        accessibility TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS review (
        id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES account(id),
        restaurant_id INTEGER REFERENCES restaurant(id),
        posted_on TIMESTAMPTZ DEFAULT NOW(),
        content TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS event (
        id SERIAL PRIMARY KEY,
        name TEXT,
        restaurant_id INTEGER REFERENCES restaurant(id),
        posted_on TIMESTAMPZ DEFAULT NOW(),
        account_id INTEGER REFERENCES account(id),
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
        event_date DATETIME
    )"""
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
