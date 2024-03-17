from invoke import task
from src.db_module import create_tables as db_create_tables


@task
def start(c):
    c.run('flask --app src/app run', pty=True)


@task
def build(c):
    db_create_tables()
