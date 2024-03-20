from flask import redirect, render_template, request
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map_view():
    return render_template("map_page.html", mappi="test_map_markers.html")


@app.route("/map2")
def map2_view():
    return render_template("test_map_markers.html")
