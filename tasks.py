from invoke import task
from src.db_setup import create_tables as db_create_tables, drop_tables as db_drop_tables, insert_restaurant



@task
def start(c):
    c.run('flask --app src/app run', pty=True)


@task
def dev(c):
    c.run('flask --app src/app --debug run', pty=True)


@task
def build(c):
    db_create_tables()


@task
def clean(c):
    db_drop_tables()


@task
def fill(c):
    insert_restaurant()
