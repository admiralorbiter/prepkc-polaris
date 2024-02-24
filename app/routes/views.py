from flask import render_template
from app import app, db
from app.models import Session

# Home Page
@app.route("/", methods=["GET"])
def index():
    sessions_data = Session.query.all()  # Fetch all session records from the database
    return render_template("sessions.html", sessions=sessions_data)
    # return render_template("index.html")

@app.route("/sessions", methods=["GET"])
def sessions():
    sessions_data = Session.query.all()  # Fetch all session records from the database
    return render_template("sessions.html", sessions=sessions_data)