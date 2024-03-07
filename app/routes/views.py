from flask import redirect, render_template, request, url_for
from app import app, db
from app.models import Session, User, Schools
from datetime import datetime, timedelta
from flask import session
from sqlalchemy import func, or_, and_, case

# Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/kcps", methods=["GET"])
def kcps():
    return render_template("/districts/kcps/kcps.html")

@app.route("/kcps/report", methods=["GET"])
def kcps_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/kcps/kcps_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/kcps/teacher_report", methods=["GET"])
def kcps_teacher_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/kcps/kcps_teacher_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/kck", methods=["GET"])
def kck():
    return render_template("/districts/kck/kck.html")

@app.route("/center", methods=["GET"])
def center():
    return render_template("/districts/center/center.html")

@app.route("/hickman", methods=["GET"])
def hickman():
    return render_template("/districts/hickman/hickman.html")

@app.route("/grandview", methods=["GET"])
def grandview():
    return render_template("/districts/grandview/grandview.html")

@app.route("/load-district-table", methods=["GET"])
def load_districts_table():
    one_year_ago = datetime.now() - timedelta(days=365)

    # Get sorting parameters
    sort_column = request.args.get('sort', 'date')  # Default sort column
    sort_direction = request.args.get('direction', 'asc')  # Default sort direction

    district = request.args.get('district')
    district_map = {
        "kck": "KANSAS CITY USD 500",
        "kcps": "KANSAS CITY PUBLIC SCHOOL DISTRICT",
        "center": "CENTER 58 SCHOOL DISTRICT",
        "hickman": "HICKMAN MILLS C-1",
        "grandview": "GRANDVIEW C-4"
    }
    district_name = district_map.get(district, district)  # Fallback to using the district arg directly if not found in the map

    # Subquery to select distinct session IDs within the specified district
    subquery = Session.query \
        .with_entities(Session.session_id, func.min(Session.id).label('min_id')) \
        .filter(Session.date >= one_year_ago, Session.district_or_company == district_name) \
        .group_by(Session.session_id) \
        .subquery()

    # Main query that joins the subquery and filters by the district
    main_query = Session.query \
        .join(subquery, Session.session_id == subquery.c.session_id) \
        .filter(Session.id == subquery.c.min_id)

    # Apply sorting to the main query
    if sort_direction == 'asc':
        main_query = main_query.order_by(getattr(Session, sort_column).asc())
    else:
        main_query = main_query.order_by(getattr(Session, sort_column).desc())

    session_data = main_query.all()

    return render_template("district_table.html", sessions=session_data)

sort_order = case(
    (Schools.level == 'Elem', 0),
    (Schools.level == 'Middle', 1),
    (Schools.level == 'High', 2),
    else_=3
)

@app.route("/load-district-summary", methods=["GET"])
def load_district_summary():
    district = request.args.get('district')
     # Get start_date and end_date from request, use default if not provided
    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    if district=="kck":
        session_data = Session.query.filter_by(district_or_company="KANSAS CITY USD 500").all()
        # Needs Updated to be Like kcps
    elif district=="kcps":
        summary_data = db.session.query(
            Session.school, 
            Schools.level,  # Assuming the School model has a 'level' field
            func.count(Session.id).label('total_sessions')
            ).join(
                Schools, Session.school == Schools.school  # This joins the Session and School models on the school name
            ).filter(
                Session.district_or_company == "KANSAS CITY PUBLIC SCHOOL DISTRICT",
                Session.status == "Completed",
                Session.date.between(start_date, end_date)
            ).group_by(
                Session.school, Schools.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    elif district=="center":
        session_data = Session.query.filter_by(district_or_company="CENTER 58 SCHOOL DISTRICT").all()
        # Needs Updated to be Like kcps
    elif district=="hickman":
        session_data = Session.query.filter_by(district_or_company="HICKMAN MILLS C-1").all()
        # Needs Updated to be Like kcps
    elif district=="grandview":
        session_data = Session.query.filter_by(district_or_company="GRANDVIEW C-4").all()
        # Needs Updated to be Like kcps
    else:
        session_data = Session.query.filter_by(district_or_company=district).all()
        # Needs Updated to be Like kcps
    return render_template("district_summary.html", summary_data=summary_data)


@app.route("/load-teacher-summary", methods=["GET"])
def load_teacher_summary():
    district = request.args.get('district')
    # Get start_date and end_date from request, use default if not provided
    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    if district=="kck":
        session_data = Session.query.filter_by(district_or_company="KANSAS CITY USD 500").all()
        # Needs Updated to be Like kcps
    elif district=="kcps":
        teacher_summary_data = Session.query \
            .filter_by(district_or_company="KANSAS CITY PUBLIC SCHOOL DISTRICT") \
            .filter(Session.status == "Completed") \
            .filter(Session.date.between(start_date, end_date)) \
            .group_by(Session.name, Session.school, Session.district_or_company) \
            .with_entities(
                Session.name,
                Session.school,
                Session.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(Session.id).label('total_sessions')
            ) \
            .all()
    elif district=="center":
        session_data = Session.query.filter_by(district_or_company="CENTER 58 SCHOOL DISTRICT").all()
        # Needs Updated to be Like kcps
    elif district=="hickman":
        session_data = Session.query.filter_by(district_or_company="HICKMAN MILLS C-1").all()
        # Needs Updated to be Like kcps
    elif district=="grandview":
        session_data = Session.query.filter_by(district_or_company="GRANDVIEW C-4").all()
        # Needs Updated to be Like kcps
    else:
        session_data = Session.query.filter_by(district_or_company=district).all()
        # Needs Updated to be Like kcps
    return render_template("teacher_summary.html", teacher_summary_data=teacher_summary_data)

@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter_by(status=status_filter).all()
    else:
        sessions_data = Session.query.all()
    return render_template("sessions.html", sessions=sessions_data)
    # return render_template("index.html")

@app.route('/edit-session', methods=['GET'])
def edit_session():
    session_id = request.args.get('session_id')
    session = Session.query.filter_by(session_id=session_id).first()
    if session:
        return render_template('edit_session_form.html', session=session)
    else:
        return 'Session not found', 404

@app.route('/delete-session', methods=['DELETE'])
def delete_session():
    session_id = request.args.get('session_id')
    session = Session.query.filter_by(session_id=session_id).first()
    if session:
        db.session.delete(session)
        db.session.commit()
        return '', 200  # Return an empty response with a 200 OK status
    else:
        return 'Session not found', 404  # Return a 404 if the session doesn't exist

@app.route('/clear-edit-pane', methods=['GET'])
def clear_edit_pane():
    return '<div id="editPane" class="edit-pane"></div>'  # Returns an empty response to clear the pane

@app.route('/update-session', methods=['POST'])
def update_session():
    print(request.form)
    session_id = request.form['session_id']
    # Fetch the session object using session_id
    session = Session.query.filter_by(session_id=session_id).first()
    try:
        if session:
            # Update session with the new data
            session.title = request.form['title']
            session.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            session.status = request.form['status']
            session.school = request.form['school']
            session.district_or_company = request.form['district_or_company']
            # Commit the changes to the database
            db.session.commit()
            # Return the updated session row in a non-editable format
            # return render_template('session_row.html', session=session)
            updated_row = render_template('session_row.html', session=session)
            
            # Script to clear the edit pane
            clear_script = "<script>document.getElementById('editPane').innerHTML = '';</script>"

            # Combine the updated row and script
            combined_response = updated_row + clear_script

            return combined_response
        else:
            return 'Session not found', 404
    except Exception as e:
        print(e)  # Log the error for debugging
        return 'Error processing request', 400

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

    # Get sorting parameters
    sort_column = request.args.get('sort', 'date')  # Default sort column
    sort_direction = request.args.get('direction', 'asc')  # Default sort direction
    upcoming = request.args.get('status', 'confirmed')

    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    # Subquery to select distinct session IDs with the earliest record based on ID
    subquery = Session.query \
        .with_entities(Session.session_id, func.min(Session.id).label('min_id')) \
        .filter(Session.date >= start_date, Session.date <= end_date) \
        .filter(Session.date >= one_year_ago) \
        .group_by(Session.session_id) \
        .subquery()

    # Main query that joins the subquery
    main_query = Session.query \
        .join(subquery, Session.session_id == subquery.c.session_id) \
        .filter(Session.id == subquery.c.min_id)

    if upcoming == 'confirmed':
        main_query = main_query.filter(Session.status == 'Confirmed')
    elif upcoming == 'request':
        main_query = main_query.filter(Session.status == 'Requested')

    # Apply sorting to the main query
    if sort_direction == 'asc':
        main_query = main_query.order_by(getattr(Session, sort_column).asc())
    else:
        main_query = main_query.order_by(getattr(Session, sort_column).desc())

    sessions_data = main_query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    one_year_ago = datetime.now() - timedelta(days=365)
    status_filter = request.args.get('statusFilter')

    # Subquery to select distinct session IDs with the earliest record based on ID
    subquery = Session.query \
        .with_entities(Session.session_id, func.min(Session.id).label('min_id')) \
        .filter(Session.date >= one_year_ago) \
        .group_by(Session.session_id) \
        .subquery()

    # Main query that joins the subquery
    main_query = Session.query \
        .join(subquery, Session.session_id == subquery.c.session_id) \
        .filter(Session.id == subquery.c.min_id)

    # Apply status filter to the main query if a filter is provided
    if status_filter:
        main_query = main_query.filter(Session.status.ilike(f"%{status_filter}%"))

    sessions_data = main_query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route('/get-sessions-by-month')
def monthly_breakdown():
    # Get the selected year from query parameters, default to current year if not specified
    year = request.args.get('year', default=2023, type=int)

    start_year = str(year)  # The starting year of the academic year
    end_year = str(year + 1)  # The ending year of the academic year
    print(start_year, end_year)

    sessions_by_month = db.session.query(func.strftime('%m', Session.date), func.count(Session.id)) \
        .filter(or_(
            and_(func.strftime('%Y', Session.date) == start_year, func.strftime('%m', Session.date) >= '07'),
            and_(func.strftime('%Y', Session.date) == end_year, func.strftime('%m', Session.date) <= '06')
        )) \
        .filter(Session.status == 'Confirmed') \
        .group_by(func.strftime('%m', Session.date)) \
        .all()
    # Convert sessions_by_month to a more usable structure if needed, e.g., a dict with month names as keys
    sorted_sessions_by_month = sorted(sessions_by_month, key=lambda x: (x[0] < '07', x[0]))

    return render_template('monthlybreakdown.html', sessions_by_month=sorted_sessions_by_month)


@app.route("/filter-kcps", methods=["GET"])
def filter_kcps():
    one_year_ago = datetime.now() - timedelta(days=365)

    # Update session with current filters if provided, else use existing session values
    if 'statusFilter' in request.args:
        session['statusFilter'] = request.args.get('statusFilter')
    if 'schoolFilter' in request.args:
        session['schoolFilter'] = request.args.get('schoolFilter')

    # Use session values for filters if available
    status_filter = session.get('statusFilter', '')
    school_filter = session.get('schoolFilter', '')

    # Start with a base query
    query = Session.query.filter(Session.date >= one_year_ago, Session.district_or_company.ilike("KANSAS CITY PUBLIC SCHOOL DISTRICT"))

    # Apply status filter if present
    if status_filter:
        query = query.filter(Session.status.ilike(f"%{status_filter}%"))

    # Apply school filter if present
    if school_filter:
        query = query.filter(Session.school.ilike(f"%{school_filter}%"))  # Adjust field name as necessary

    # Execute the query
    sessions_data = query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route("/clear-filters", methods=["GET"])
def clear_filters():
    session.pop('statusFilter', None)  # Remove the filter from the session if it exists
    session.pop('schoolFilter', None)
    return redirect(url_for('filter_kcps'))  # Redirect back to the filter page or wherever appropriate

@app.route("/session_details", methods=["GET"])
def session_details():
    session_id = request.args.get('session_id')
    session_data = Session.query.filter_by(session_id=session_id).all()
    print(session_data)
    return render_template("session_details.html", sessions=session_data)