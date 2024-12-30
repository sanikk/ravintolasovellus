from datetime import date
from app import db
from sqlalchemy import text


#################################
# ACCOUNTS                      #
#################################


def create_user(username: str, firstname: str, lastname: str, password_hash: str):
    if not (username and password_hash):
        return None
    sql = "INSERT INTO accounts (username, firstname, lastname, password) VALUES (:username, :firstname, :lastname, :password) RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "password": password_hash,
        },
    )
    db.session.commit()
    return ret.scalar()


def get_accounts_all():
    sql = "SELECT * FROM accounts"
    return db.session.execute(text(sql)).fetchall()


def get_account_by_username(username: str):
    sql = (
        "SELECT id,username,firstname,lastname FROM accounts WHERE username = :username"
    )
    user = db.session.execute(text(sql), {"username": username}).fetchone()
    return user


def get_accountWithPassword_by_username(username: str):
    sql = "SELECT id,username,password,firstname,lastname FROM accounts WHERE username = :username"
    user = db.session.execute(text(sql), {"username": username}).fetchone()
    return user


def get_account_by_id(account_id: int):
    sql = (
        "SELECT id, username, firstname, lastname FROM accounts WHERE id = :account_id"
    )
    user = db.session.execute(text(sql), {"account_id": account_id}).fetchone()
    return user


#####################################
# RESTAURANTS                       #
#####################################


def get_restaurants_all():
    sql = "SELECT * FROM restaurants"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_by_id(restaurant_id: int):
    sql = "SELECT id, name, account_id, latitude, longitude, place_id, address FROM restaurants WHERE id = :restaurant_id"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


def get_restaurants_by_accountId(account_id: int):
    return db.session.execute(
        text(
            "SELECT id, name, account_id, latitude, longitude, place_id, address FROM restaurants WHERE account_id = :account_id"
        ),
        {"account_id": account_id},
    ).fetchall()


def create_restaurant(
    name: str, account_id: int, address: str, lat: float, long: float, place_id: int
):
    if not (name and account_id and address and lat and long and place_id):
        return None
    sql = "INSERT INTO restaurants (name, account_id, address, latitude, longitude, place_id) VALUES (:name, :account_id, :address, :lat, :long, :place_id) RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "account_id": account_id,
            "address": address,
            "lat": lat,
            "long": long,
            "place_id": place_id,
        },
    )
    db.session.commit()
    return ret.scalar()


def get_accountId_by_restaurantId(restaurant_id: int):
    return db.session.execute(
        text("SELECT account_id FROM restaurants WHERE id=:restaurant_id"),
        {"restaurant_id": restaurant_id},
    ).fetchone()


def update_restaurant_by_id(
    restaurant_id: int, name, address, latitude, longitude, place_id
):
    sql = "UPDATE restaurants SET name=:name, address=:address, latitude=:latitude, longitude=:longitude, place_id=:place_id WHERE id=:restaurant_id"
    db.session.execute(
        text(sql),
        {
            "restaurant_id": restaurant_id,
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "place_id": place_id,
        },
    )
    db.session.commit()


def delete_restaurant_by_id(restaurant_id: int):
    db.session.execute(
        text("DELETE FROM restaurants WHERE id=:restaurant_id"),
        {"restaurant_id": restaurant_id},
    )
    db.session.commit()


#############################################
#   RATINGS                                 #
#############################################


def get_ratings_all():
    sql = "SELECT * FROM ratings"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_by_id(rating_id: int):
    sql = "SELECT * FROM ratings WHERE id = :rating_id"
    return db.session.execute(text(sql), {"rating_id": rating_id}).fetchone()


def get_ratings_by_accountId(account_id: int):
    sql = "SELECT * FROM ratings WHERE account_id = :account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()


#################################################
# EVENTS                                        #
#################################################


def get_events_all():
    sql = "SELECT * FROM events"
    return db.session.execute(text(sql)).fetchall()


def get_events_by_id(event_id: int):
    sql = "SELECT * FROM events WHERE id=:event_id"
    return db.session.execute(text(sql), {"event_id": event_id}).fetchone()


def get_events_by_accountId(account_id: int):
    sql = "SELECT * FROM EVENTS WHERE account_id = :account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()


def create_event(name: str, restaurant_id: int, event_date: date, account_id: int):
    if not (name and account_id):
        return None
    sql = "INSERT INTO events (name, restaurant_id, event_date, account_id) VALUES (:name, :restaurant_id, :event_date, :account_id) RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "restaurant_id": restaurant_id,
            "event_date": event_date,
            "account_id": account_id,
        },
    )
    db.session.commit()
    return ret.scalar()
