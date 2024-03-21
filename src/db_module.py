from app import db
from sqlalchemy import text


def get_all_accounts():
    sql = "SELECT * FROM account"
    return db.session.execute(text(sql)).fetchall()


def get_all_restaurants():
    sql = "SELECT * FROM restaurant"
    return db.session.execute(text(sql)).fetchall()


def get_all_reviews():
    sql = "SELECT * FROM review"
    return db.session.execute(text(sql)).fetchall()
