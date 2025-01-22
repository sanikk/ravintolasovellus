# from datetime import date
from app import db
from sqlalchemy import text

#################################
# ACCOUNTS                      #
#################################


# id, active, username, password, email, billing_info, firstname, lastname, description
def create_user(
    username: str,
    password_hash: str,
    email: str,
    billing_info: str,
    firstname: str,
    lastname: str,
    description: str,
):
    if not (username and password_hash):
        return None
    sql = "INSERT INTO accounts (active, username, password, email, billing_info, firstname, lastname, description) \
            VALUES (TRUE, :username, :password, :email, :billing_info, :firstname, :lastname, :description) \
            RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "username": username,
            "password": password_hash,
            "email": email,
            "billing_info": billing_info,
            "firstname": firstname,
            "lastname": lastname,
            "description": description,
        },
    )
    db.session.commit()
    return ret.scalar()


def update_account_by_id(
    account_id: int,
    username: str,
    email: str,
    billing_info: str,
    firstname: str,
    lastname: str,
    description: str,
    password_hash=None,
):
    if not account_id or not (
        username
        or email
        or billing_info
        or firstname
        or lastname
        or description
        or password_hash
    ):
        return None
    sql = "UPDATE accounts SET "
    param_list = []
    valuedict = {}
    if username:
        param_list.append("username=:username")
        valuedict["username"] = username
    if password_hash:
        param_list.append("password=:password")
        valuedict["password"] = password_hash
    if email:
        param_list.append("email=:email")
        valuedict["email"] = email
    if billing_info:
        param_list.append("billing_info=:billing_info")
        valuedict["billing_info"] = billing_info
    if firstname:
        param_list.append("firstname=:firstname")
        valuedict["firstname"] = firstname
    if lastname:
        param_list.append("lastname=:lastname")
        valuedict["lastname"] = lastname
    if description:
        param_list.append("description=:description")
        valuedict["description"] = description
    valuedict["account_id"] = account_id
    sql += ",".join(param_list) + " WHERE id=:account_id AND active = TRUE RETURNING id"
    # print(f"{sql=}")
    ret = db.session.execute(text(sql), valuedict)
    db.session.commit()
    return ret


def get_account_by_username(username: str):
    sql = "SELECT id,username,password,firstname,lastname FROM accounts WHERE username = :username AND active = TRUE"
    user = db.session.execute(text(sql), {"username": username}).fetchone()
    return user


def get_account_by_id(account_id: int):
    sql = "SELECT id, username, email, billing_info, firstname, lastname, description FROM accounts WHERE id = :account_id AND active = TRUE"
    user = db.session.execute(text(sql), {"account_id": account_id}).fetchone()
    return user


def check_account_email(email: str):
    sql = "SELECT email FROM accounts WHERE email=:email"
    return db.session.execute(text(sql), {"email": email}).fetchone()


def delete_user_by_id(account_id: int):
    return db.session.execute(
        text(
            "UPDATE accounts SET active=FALSE WHERE id=:account_id AND active = TRUE RETURNING id"
        ),
        {"account_id": account_id},
    ).fetchone()


#####################################
# RESTAURANTS                       #
#####################################


def get_restaurants_all():
    sql = "SELECT * FROM restaurants WHERE active = TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_list():
    sql = "SELECT id, name,address FROM restaurants WHERE active = TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_restaurants_by_id(restaurant_id: int):
    sql = "SELECT r.id, r.name, r.account_id, a.firstname AS account_firstname, a.lastname AS account_lastname, \
                r.latitude, r.longitude, r.place_id, r.address, r.description \
            FROM restaurants r JOIN accounts a ON r.account_id = a.id \
            WHERE r.id = :restaurant_id AND r.active = TRUE"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchone()


def get_restaurants_by_accountId(account_id: int):
    return db.session.execute(
        text(
            "SELECT id, name, latitude, longitude, place_id, address \
            FROM restaurants \
            WHERE account_id = :account_id AND active = TRUE"
        ),
        {"account_id": account_id},
    ).fetchall()


def create_restaurant(
    name: str,
    account_id: int,
    address: str,
    lat: float,
    long: float,
    place_id: int,
    description: str,
):
    if not (name and account_id and address and lat and long and place_id):
        return None
    sql = "INSERT INTO restaurants (active, name, account_id, address, latitude, longitude, place_id, description) \
                            VALUES (TRUE, :name, :account_id, :address, :lat, :long, :place_id, :description) RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "account_id": account_id,
            "address": address,
            "lat": lat,
            "long": long,
            "place_id": place_id,
            "description": description,
        },
    )
    db.session.commit()
    return ret.scalar()


def get_accountId_by_restaurantId(restaurant_id: int):
    return db.session.execute(
        text(
            "SELECT account_id \
            FROM restaurants \
            WHERE id=:restaurant_id AND active = TRUE"
        ),
        {"restaurant_id": restaurant_id},
    ).scalar()


def update_restaurant_by_id(
    restaurant_id: int, name, address, latitude, longitude, place_id, description
):
    sql = "UPDATE restaurants \
            SET name=:name, address=:address, latitude=:latitude, longitude=:longitude, place_id=:place_id, description=:description \
            WHERE id=:restaurant_id AND active = TRUE"
    db.session.execute(
        text(sql),
        {
            "restaurant_id": restaurant_id,
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "place_id": place_id,
            "description": description,
        },
    )
    db.session.commit()


def delete_restaurant_by_id(restaurant_id: int):
    db.session.execute(
        text(
            "UPDATE restaurants \
            SET active=FALSE \
            WHERE restaurant_id=:restaurant_id"
        ),
        {"restaurant_id": restaurant_id},
    )
    db.session.commit()


#############################################
#   RATINGS                                 #
#############################################


def get_ratings_all():
    sql = "SELECT * FROM ratings WHERE active = TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_list():
    sql = "SELECT rat.id, rat.rating, rat.account_id, acc.firstname AS account_firstname, \
                acc.lastname AS account_lastname, rat.restaurant_id, res.name AS restaurant_name, rat.posted_on \
            FROM ratings rat JOIN restaurants res ON rat.restaurant_id = res.id JOIN accounts acc ON rat.account_id = acc.id\
            WHERE rat.active=TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_ratings_by_id(rating_id: int):
    sql = "SELECT rat.*, res.name as restaurant_name, a.firstname AS account_firstname, a.lastname AS account_lastname \
            FROM ratings rat JOIN restaurants res ON rat.restaurant_id = res.id JOIN accounts a ON rat.account_id = a.id \
            WHERE rat.id = :rating_id AND rat.active = TRUE"
    return db.session.execute(text(sql), {"rating_id": rating_id}).fetchone()


def get_ratings_by_accountId(account_id: int):
    sql = "WITH last_reviews AS (SELECT rat.id, rat.restaurant_id, res.name as restaurant_name, TO_CHAR(rat.posted_on, 'DD.MM.YYYY HH24:MM:SS') AS posted_on, rat.rating \
            FROM ratings rat JOIN restaurants res ON rat.restaurant_id = res.id WHERE rat.account_id=:account_id ORDER BY rat.posted_on LIMIT 10) \
                SELECT (SELECT COUNT(rating) FROM ratings WHERE account_id=:account_id) AS total_reviews, \
                       (SELECT COALESCE(AVG(rating), 0) FROM ratings WHERE account_id=:account_id) AS average_rating, \
                        json_agg(last_reviews.*) AS last_reviews \
                FROM last_reviews"
    #     sql = "SELECT rat.id, rat.restaurant_id, rat.rating, rat.posted_on, res.name AS restaurant_name \
    #             FROM ratings rat JOIN restaurants res ON rat.restaurant_id = res.id \
    #             WHERE rat.account_id = :account_id AND rat.active = TRUE"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchone()


def get_ratings_by_restaurantId(restaurant_id: int):
    sql = "SELECT ra.id, ra.account_id, a.firstname as account_firstname, a.lastname AS account_lastname, ra.restaurant_id, ra.posted_on, ra.rating \
        FROM ratings ra JOIN accounts a ON ra.account_id = a.id \
        WHERE restaurant_id=:restaurant_id AND ra.active=TRUE"
    return db.session.execute(text(sql), {"restaurant_id": restaurant_id}).fetchall()


#################################################
# EVENTS                                        #
#################################################


def get_events_all():
    sql = "SELECT * FROM events WHERE active = TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_events_list():
    sql = "SELECT e.id, e.name, e.restaurant_id, r.name AS restaurant_name \
            FROM events e JOIN restaurants r ON e.restaurant_id = r.id \
            WHERE active = TRUE"
    return db.session.execute(text(sql)).fetchall()


def get_events_list_by_accountId(account_id: int):
    sql = "SELECT e.id, e.name, e.start_time, e.end_time, e.restaurant_id, r.name AS restaurant_name \
            FROM events e JOIN restaurants r ON e.restaurant_id = r.id \
            WHERE e.account_id=:account_id OR r.account_id=:account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()


def get_events_by_id(event_id: int):
    sql = "SELECT * FROM events WHERE id=:event_id"
    return db.session.execute(text(sql), {"event_id": event_id}).fetchone()


def get_events_by_accountId(account_id: int):
    sql = "SELECT * FROM EVENTS WHERE account_id = :account_id"
    return db.session.execute(text(sql), {"account_id": account_id}).fetchall()


def get_events_by_restaurantId(restaurant_id: int):
    return db.session.execute(
        text("SELECT * FROM events WHERE restaurant_id=:restaurant_id"),
        {"restaurant_id": restaurant_id},
    ).fetchall()


def create_event(
    name: str,
    restaurant_id: int,
    account_id: int,
    start_time,
    end_time,
    description: str,
):
    if not (name and account_id):
        return None
    sql = "INSERT INTO events (name, restaurant_id, account_id, start_time, end_time, description) \
            VALUES (:name, :restaurant_id, :account_id, :start_time, :end_time, :description) \
            RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "restaurant_id": restaurant_id,
            "account_id": account_id,
            "start_time": start_time,
            "end_time": end_time,
            "description": description,
        },
    )
    db.session.commit()
    return ret.scalar()


#################################
# BUFFETS                       #
#################################


def get_buffets_all():
    return db.session.execute(
        text("SELECT * FROM buffets WHERE active = TRUE")
    ).fetchall()


def get_buffets_by_id(buffet_id: int):
    return db.session.execute(
        text(
            "SELECT b.*,r.name as restaurant_name,r.account_id FROM buffets b JOIN restaurants r ON b.restaurant_id = r.id WHERE b.id=:buffet_id AND b.active = TRUE"
        ),
        {"buffet_id": buffet_id},
    ).fetchone()


def get_buffets_by_restaurantId(restaurant_id: int):
    return db.session.execute(
        text(
            "SELECT id,name FROM buffets WHERE restaurant_id=:restaurant_id AND active = TRUE"
        ),
        {"restaurant_id": restaurant_id},
    ).fetchall()


def create_buffet(
    name, account_id, restaurant_id, days, starttime, endtime, price, description
):
    # return None
    sql = "INSERT INTO buffets (name, restaurant_id, starttime, endtime, monday, tuesday,wednesday, thursday, friday, saturday, sunday, price, description) \
            VALUES (:name, :restaurant_id, :starttime, :endtime, :Monday, :Tuesday, :Wednesday, :Thursday, :Friday, :Saturday, :Sunday, :price, :description) \
            RETURNING id"
    ret = db.session.execute(
        text(sql),
        {
            "name": name,
            "account_id": account_id,
            "restaurant_id": restaurant_id,
            "starttime": starttime,
            "endtime": endtime,
            **days,
            "price": price,
            "description": description,
        },
    )
    db.session.commit()
    return ret.scalar()
