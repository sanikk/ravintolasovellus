from invoke.tasks import task
from secrets import token_hex
from src.db_filler import fill_db


@task
def start(c):
    c.run("flask --app src/app run")


@task
def dev(c):
    c.run("flask --app src/app --debug run", pty=True)


@task
def build(c):
    c.run("sqlite3 database.db < src/schema.sql")
    with open(".env", "w") as fo:
        fo.write(f"FLASK_SECRET_KEY={token_hex(16)}")
    fill_db()
