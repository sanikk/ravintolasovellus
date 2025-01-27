CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active BOOL DEFAULT TRUE,
    username VARCHAR(32) UNIQUE,
    password VARCHAR(256),
    email VARCHAR(64) UNIQUE,
    billing_info VARCHAR(256),
    firstname VARCHAR(32),
    lastname VARCHAR(32),
    description VARCHAR(500)
);
    
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active BOOL DEFAULT TRUE,
    name VARCHAR(64),
    account_id INTEGER,
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
    sundayend TIME,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE INDEX idx_account_active ON restaurants (account_id, active);


CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active BOOL DEFAULT TRUE,
    account_id INTEGER,
    restaurant_id INTEGER,
    posted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    content VARCHAR(500),
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);


CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active BOOL DEFAULT FALSE,
    name VARCHAR(128),
    restaurant_id INTEGER,
    posted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    description VARCHAR(500),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS buffets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active BOOL DEFAULT TRUE,
    restaurant_id INTEGER,
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
    description VARCHAR(500),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);    
