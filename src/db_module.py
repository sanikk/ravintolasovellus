from app import db
from sqlalchemy import text

from werkzeug.security import check_password_hash, generate_password_hash


def create_user(username: str, password: str):
    sql = "INSERT INTO accounts (username, password) VALUES (:username, :password)"
    le_hash = generate_password_hash(password)
    db.session.execute(text(sql), {"username": username, "password": le_hash})
    db.session.commit()


def check_username_and_password(username: str, password: str):
    sql = "SELECT id, username, password, firstname, lastname FROM accounts WHERE username=:username"
    user = db.session.execute(text(sql), {"username": username}).fetchone()
    if not user:
        # TODO: show error to user
        return
    if check_password_hash(user.password, password):
        # TODO: great success!
        return id, user.username, user.firstname or user.lastname
    # TODO: inform user of failure
    return


def get_accounts_all():
    sql = "SELECT * FROM accounts"
    return db.session.execute(text(sql)).fetchall()


def get_account_by_username(username: str):
    sql = "SELECT * FROM accounts WHERE username = :username"
    return db.session.execute(text(sql), {"username": username})


def get_account_by_user_id(user_id: int):
    sql = "SELECT * FROM accounts WHERE id = :user_id"
    return db.session.execute(text(sql), {"user_id": user_id})


def get_restaurants_all():
    sql = "SELECT * FROM restaurants"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_single(restaurant_id: int):
    sql = "SELECT name, latitude, longitude, place_id, address FROM restaurants WHERE id = :restaurant_id"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


def get_ratings_all():
    sql = "SELECT * FROM ratings"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_single(rating_id: int):
    sql = "SELECT * FROM ratings WHERE id = :rating_id"
    return db.session.execute(text(sql), {"rating_id": rating_id}).fetchone()
