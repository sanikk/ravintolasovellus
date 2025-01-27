from os import getenv
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")
