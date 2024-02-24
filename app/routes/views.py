from flask import render_template, request
from app import app
from app.models import Session, User
from datetime import datetime, timedelta

# Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/districts/kck", methods=["GET"])
def kck():
    return render_template("/districts/kck.html")

@app.route("/districts/kcps", methods=["GET"])
def kcps():
    return render_template("/districts/kcps.html")

@app.route("/districts/center", methods=["GET"])
def center():
    return render_template("/districts/center.html")

@app.route("/districts/hickman", methods=["GET"])
def hickman():
    return render_template("/districts/hickman.html")

@app.route("/districts/grandview", methods=["GET"])
def grandview():
    return render_template("/districts/grandview.html")

@app.route("/load-district-table", methods=["GET"])
def load_districts_table():
    print(request.args.get('district'))
    district = request.args.get('district')
    if district=="kck":
        session_data = Session.query.filter_by(district_or_company="KANSAS CITY USD 500").all()
    elif district=="kcps":
        session_data = Session.query.filter_by(district_or_company="KANSAS CITY PUBLIC SCHOOL DISTRICT").all()
    elif district=="center":
        session_data = Session.query.filter_by(district_or_company="CENTER 58 SCHOOL DISTRICT").all()
    elif district=="hickman":
        session_data = Session.query.filter_by(district_or_company="HICKMAN MILLS C-1").all()
    elif district=="grandview":
        session_data = Session.query.filter_by(district_or_company="GRANDVIEW C-4").all()
    else:
        session_data = Session.query.filter_by(district_or_company=district).all()
    return render_template("session_table.html", sessions=session_data)

@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter_by(status=status_filter).all()
    else:
        sessions_data = Session.query.all()
    return render_template("sessions.html", sessions=sessions_data)
    # return render_template("index.html")

@app.route("/users", methods=["GET"])
def users():
    user_data=User.query.all()
    return render_template("users.html", users=user_data)

@app.route("/load-user-table", methods=["GET"])
def load_users_table():
    user_data=User.query.all()
    return render_template("user_table.html", users=user_data)

@app.route("/load-sessions-table", methods=["GET"])
def load_sessions_table():
    one_year_ago = datetime.now() - timedelta(days=365)

    sort_column = request.args.get('sort', 'date')  # Assuming 'date' is a valid attribute of Session
    if request.args.get('sort'):
        sort_column = request.args.get('sort')
    sort_direction = request.args.get('direction', 'asc')  # Default direction
    # Build the base query
    query = Session.query.filter(Session.date >= one_year_ago)

    # Apply sorting
    if sort_direction == 'asc':
        query = query.order_by(getattr(Session, sort_column).asc())
    else:
        query = query.order_by(getattr(Session, sort_column).desc())

    sessions_data = query.all()
    # print(query)
    return render_template("session_table.html", sessions=sessions_data)

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    one_year_ago = datetime.now() - timedelta(days=365)
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter(Session.date >= one_year_ago, Session.status.ilike(f"%{status_filter}%")).all()
    else:
        sessions_data = Session.query.filter(Session.date >= one_year_ago).all()
    return render_template("session_table.html", sessions=sessions_data)