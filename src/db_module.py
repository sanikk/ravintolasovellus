from app import db
from sqlalchemy import text


def get_all_accounts():
    sql = "SELECT * FROM account"
    return db.session.execute(text(sql)).fetchall()


def get_all_restaurants():
    sql = "SELECT id, name, latitude, longitude FROM restaurant"
    return db.session.execute(text(sql)).fetchall()


def get_single_restaurant(restaurant_id: int):
    sql = "SELECT name, latitude, longitude, place_id, address FROM restaurant WHERE id = :restaurant_id"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


def get_all_reviews():
    sql = "SELECT * FROM review"
    return db.session.execute(text(sql)).fetchall()
