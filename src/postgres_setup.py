from psycopg import connect
from psycopg.sql import SQL, Identifier
from src.config import DATABASE_NAME


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
        active BOOL DEFAULT TRUE,
        username VARCHAR(32) UNIQUE,
        password VARCHAR(256),
        email VARCHAR(64) UNIQUE,
        billing_info VARCHAR(256),
        firstname VARCHAR(32),
        lastname VARCHAR(32),
        description VARCHAR(500)
    )"""
    cur.execute(sql)
    # TODO: make this dynamic
    sql = """CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        active BOOL DEFAULT TRUE,
        name VARCHAR(64),
        account_id INTEGER REFERENCES accounts(id),
        latitude FLOAT,
        longitude FLOAT,
        place_id VARCHAR(20),
        address VARCHAR(128),
        description VARCHAR(500),
        mondaystart TIME,
        mondayend TIME,
        tuesdaystart TIME,
        tuesdayend TIME,
        wednesdaystart TIME,
        wednesdayend TIME,
        thursdaystart TIME,
        thursdayend TIME,
        fridaystart TIME,
        fridayend TIME,
        saturdaystart TIME,
        saturdayend TIME,
        sundaystart TIME,
        sundayend TIME
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
    # TODO: make this dynamic:
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
        price INTEGER,
        description VARCHAR(500)
    )"""
    cur.execute(sql)

    print("Database has been built")
    conn.commit()
    cur.close()
    conn.close()
