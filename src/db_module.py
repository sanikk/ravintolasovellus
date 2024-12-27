from app import db
from sqlalchemy import text

from werkzeug.security import check_password_hash, generate_password_hash


def create_user(username: str, firstname: str, lastname: str, password: str):
    sql = "INSERT INTO accounts (username, firstname, lastname, password) VALUES (:username, :firstname, :lastname, :password)"
    le_hash = generate_password_hash(password)
    ret = db.session.execute(
        text(sql),
        {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "password": le_hash,
        },
    )
    db.session.commit()


def check_username_and_password(username: str, password: str):
    sql = "SELECT id, username, password, firstname, lastname FROM accounts WHERE username=:username"
    user = db.session.execute(text(sql), {"username": username}).fetchone()
    if not user:
        return None
    if check_password_hash(user.password, password):
        return (user.id, user.username, user.firstname or user.lastname)
    return None


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


def get_restaurants_all():
    sql = "SELECT * FROM restaurants"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_single(restaurant_id: int):
    sql = "SELECT name, latitude, longitude, place_id, address FROM restaurants WHERE id = :restaurant_id"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


#        id SERIAL PRIMARY KEY,
#        name TEXT,
#        admin_id INTEGER REFERENCES accounts(id),
#        latitude FLOAT,
#        longitude FLOAT,
#        place_id TEXT,
#        address TEXT


def create_restaurant(name, admin_id, address):
    sql = "INSERT INTO restaurants (name, admin_id, address) VALUES (:name, :admin_id, :address) RETURNING id"
    ret = db.session.execute(
        text(sql), {"name": name, "admin_id": admin_id, "address": address}
    )
    db.session.commit()
    return ret.scalar()


def get_ratings_all():
    sql = "SELECT * FROM ratings"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_single(rating_id: int):
    sql = "SELECT * FROM ratings WHERE id = :rating_id"
    return db.session.execute(text(sql), {"rating_id": rating_id}).fetchone()
