from flask import render_template, request
from app import app
from app.models import Session

# Home Page
@app.route("/", methods=["GET"])
def index():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter_by(status=status_filter).all()
    else:
        sessions_data = Session.query.all()
    return render_template("sessions.html", sessions=sessions_data)
    # return render_template("index.html")

@app.route("/load-sessions-table", methods=["GET"])
def load_sessions_table():
    sessions_data = Session.query.all()
    return render_template("session_table.html", sessions=sessions_data)

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    status_filter = request.args.get('statusFilter')
    sessions_data = Session.query.filter(Session.status.ilike(f"%{status_filter}%")).all() if status_filter else Session.query.all()
    return render_template("session_table.html", sessions=sessions_data)