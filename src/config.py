from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = getenv("DATABASE_NAME")
FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")
