from flask import render_template
from app import app

import routing.accounts
import routing.restaurants
import routing.ratings
import routing.events

from service.map_service import get_map


@app.route("/")
def index():
    return render_template("map_page.html", iframe=get_map())
