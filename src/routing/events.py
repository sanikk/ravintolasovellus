from flask import render_template, request, redirect, flash, session
from app import app
from db_module import get_events_all, get_events_by_id, get_restaurants_all
from service.helper_service import add_event


@app.route("/events")
def events_page():
    events = get_events_all()
    return render_template("events_list.html", events=events)


@app.route("/events/<int:event_id>")
def single_event_page(event_id: int):
    event = get_events_by_id(event_id)
    return render_template("events_single.html", event=event)


@app.route("/events/create", methods=["POST"])
def create_event_endpoint():
    name = request.form["name"]
    restaurant_id = request.form["venue"]
    event_date = request.form["date"]
    account_id = session["user_id"]
    ret, errors = add_event(name, restaurant_id, event_date, account_id)
    [flash(error) for error in errors]
    if ret:
        return redirect(f"/events/{ret}")
    return redirect("/events/create")


@app.route("/events/new")
def create_event_form():
    restaurants = [{"id": r.id, "name": r.name} for r in get_restaurants_all()]
    return render_template("events_new.html", restaurants=restaurants)
