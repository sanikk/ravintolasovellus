from app import db
from sqlalchemy import text


#################################
# ACCOUNTS                      #
#################################


def create_user(username: str, firstname: str, lastname: str, password_hash: str):
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


def get_account_by_user_id(user_id: int):
    sql = "SELECT id, username, firstname, lastname FROM accounts WHERE id = :user_id"
    user = db.session.execute(text(sql), {"user_id": user_id}).fetchone()
    return user


#####################################
# RESTAURANTS                       #
#####################################


def get_restaurants_all():
    sql = "SELECT * FROM restaurants"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_by_id(restaurant_id: int):
    sql = "SELECT id, name, admin_id, latitude, longitude, place_id, address FROM restaurants WHERE id = :restaurant_id"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


def get_restaurants_by_admin_id(admin_id: int):
    sql = "SELECT id, name, admin_id, latitude, longitude, place_id, address FROM restaurants WHERE admin_id = :admin_id"
    return db.session.execute(text(sql), {"admin_id": admin_id}).fetchall()


def create_restaurant(name, admin_id, address, lat: float, long: float, place_id: int):
    sql = "INSERT INTO restaurants (name, admin_id, address, latitude, longitude, place_id) VALUES (:name, :admin_id, :address, :lat, :long, :place_id) RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "admin_id": admin_id,
            "address": address,
            "lat": lat,
            "long": long,
            "place_id": place_id,
        },
    )
    db.session.commit()
    return ret.scalar()


#############################################
#   RATINGS                                 #
#############################################


def get_ratings_all():
    sql = "SELECT * FROM ratings"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_by_id(rating_id: int):
    sql = "SELECT * FROM ratings WHERE id = :rating_id"
    return db.session.execute(text(sql), {"rating_id": rating_id}).fetchone()


def get_ratings_by_account_id(account_id: int):
    sql = "SELECT * FROM ratings WHERE account_id = :account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()


#################################################
# EVENTS                                        #
#################################################


def get_events_all():
    sql = "SELECT * FROM events"
    return db.session.execute(text(sql)).fetchall()


def get_events_by_account_id(account_id: int):
    sql = "SELECT * FROM EVENTS WHERE account_id = :account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()
