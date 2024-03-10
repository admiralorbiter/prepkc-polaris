from flask import redirect, render_template, request, url_for
from app import app, db
from app.models import SessionRow, User, School, Session
from datetime import datetime, timedelta
from flask import session
from sqlalchemy import func, or_, and_, case

def add_school_to_session(session_id, school_id):
    session = Session.query.get(session_id)
    school = School.query.get(school_id)
    
    # Assuming that the 'schools' relationship in the Session model is set up correctly
    session.schools.append(school)
    db.session.commit()

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

@app.route("/kck/report", methods=["GET"])
def kck_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/kck/kck_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/kck/teacher_report", methods=["GET"])
def kck_teacher_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/kck/kck_teacher_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/center", methods=["GET"])
def center():
    return render_template("/districts/center/center.html")

@app.route("/hickman", methods=["GET"])
def hickman():
    return render_template("/districts/hickman/hickman.html")

@app.route("/hickman/report", methods=["GET"])
def hickman_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/hickman/hickman_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/hickman/teacher_report", methods=["GET"])
def hickman_teacher_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/hickman/hickman_teacher_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/center/report", methods=["GET"])
def center_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/center/center_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/center/teacher_report", methods=["GET"])
def center_teacher_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/center/center_teacher_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/grandview", methods=["GET"])
def grandview():
    return render_template("/districts/grandview/grandview.html")

@app.route("/grandview/report", methods=["GET"])
def grandview_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/grandview/grandview_report.html", start_date=default_start_date, end_date=default_end_date)

@app.route("/grandview/teacher_report", methods=["GET"])
def grandview_teacher_report():
    default_start_date = datetime(2023, 7, 1).strftime('%Y-%m-%d')
    default_end_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("/districts/grandview/grandview_teacher_report.html", start_date=default_start_date, end_date=default_end_date)

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
    subquery = SessionRow.query \
        .with_entities(SessionRow.session_id, func.min(SessionRow.id).label('min_id')) \
        .filter(SessionRow.date >= one_year_ago, SessionRow.district_or_company == district_name) \
        .group_by(SessionRow.session_id) \
        .subquery()

    # Main query that joins the subquery and filters by the district
    main_query = SessionRow.query \
        .join(subquery, SessionRow.session_id == subquery.c.session_id) \
        .filter(SessionRow.id == subquery.c.min_id)

    # Apply sorting to the main query
    if sort_direction == 'asc':
        main_query = main_query.order_by(getattr(SessionRow, sort_column).asc())
    else:
        main_query = main_query.order_by(getattr(SessionRow, sort_column).desc())

    #Default Confirmed Status
    main_query = main_query.filter(SessionRow.status == 'Confirmed')

    session_data = main_query.all()

    return render_template("district_table.html", sessions=session_data)

sort_order = case(
    (School.level == 'Elem', 0),
    (School.level == 'Middle', 1),
    (School.level == 'High', 2),
    else_=3
)

@app.route("/load-district-summary", methods=["GET"])
def load_district_summary():
    district = request.args.get('district')
     # Get start_date and end_date from request, use default if not provided
    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    if district=="kck":
        summary_data = db.SessionRow.query(
        SessionRow.school, 
        School.level,  # Assuming the School model has a 'level' field
        func.count(SessionRow.id).label('total_sessions')
        ).join(
            School, SessionRow.school == School.school  # This joins the Session and School models on the school name
        ).filter(
            SessionRow.district_or_company == "KANSAS CITY USD 500",
            SessionRow.status == "Completed",
            SessionRow.date.between(start_date, end_date)
        ).group_by(
            SessionRow.school, School.level  # Group by both the school name and the school level
        ).order_by(sort_order).all()
    elif district=="kcps":
        summary_data = db.SessionRow.query(
            SessionRow.school, 
            School.level,  # Assuming the School model has a 'level' field
            func.count(SessionRow.id).label('total_sessions')
            ).join(
                School, SessionRow.school == School.school  # This joins the Session and School models on the school name
            ).filter(
                SessionRow.district_or_company == "KANSAS CITY PUBLIC SCHOOL DISTRICT",
                SessionRow.status == "Completed",
                SessionRow.date.between(start_date, end_date)
            ).group_by(
                SessionRow.school, School.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    elif district=="center":
        # Needs Updated to be Like kcps
        summary_data = db.SessionRow.query(
            SessionRow.school, 
            School.level,  # Assuming the School model has a 'level' field
            func.count(SessionRow.id).label('total_sessions')
            ).join(
                School, SessionRow.school == School.school  # This joins the Session and School models on the school name
            ).filter(
                SessionRow.district_or_company == "CENTER 58 SCHOOL DISTRICT",
                SessionRow.status == "Completed",
                SessionRow.date.between(start_date, end_date)
            ).group_by(
                SessionRow.school, School.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    elif district=="hickman":
        summary_data = db.SessionRow.query(
            SessionRow.school, 
            School.level,  # Assuming the School model has a 'level' field
            func.count(SessionRow.id).label('total_sessions')
            ).join(
                School, SessionRow.school == School.school  # This joins the Session and School models on the school name
            ).filter(
                SessionRow.district_or_company == "HICKMAN MILLS C-1",
                SessionRow.status == "Completed",
                SessionRow.date.between(start_date, end_date)
            ).group_by(
                SessionRow.school, School.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    elif district=="grandview":
        summary_data = db.SessionRow.query(
            SessionRow.school, 
            School.level,  # Assuming the School model has a 'level' field
            func.count(SessionRow.id).label('total_sessions')
            ).join(
                School, SessionRow.school == School.school  # This joins the Session and School models on the school name
            ).filter(
                SessionRow.district_or_company == "GRANDVIEW C-4",
                SessionRow.status == "Completed",
                SessionRow.date.between(start_date, end_date)
            ).group_by(
                SessionRow.school, School.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    else:
        summary_data = db.SessionRow.query(
            SessionRow.school, 
            School.level,  # Assuming the School model has a 'level' field
            func.count(SessionRow.id).label('total_sessions')
            ).join(
                School, SessionRow.school == School.school  # This joins the Session and School models on the school name
            ).filter(
                SessionRow.district_or_company == district,
                SessionRow.status == "Completed",
                SessionRow.date.between(start_date, end_date)
            ).group_by(
                SessionRow.school, School.level  # Group by both the school name and the school level
            ).order_by(sort_order).all()
    return render_template("district_summary.html", summary_data=summary_data)


@app.route("/load-teacher-summary", methods=["GET"])
def load_teacher_summary():
    district = request.args.get('district')
    # Get start_date and end_date from request, use default if not provided
    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    if district=="kck":
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company="KANSAS CITY USD 500") \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    elif district=="kcps":
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company="KANSAS CITY PUBLIC SCHOOL DISTRICT") \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    elif district=="center":
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company="CENTER 58 SCHOOL DISTRICT") \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    elif district=="hickman":
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company="HICKMAN MILLS C-1") \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    elif district=="grandview":
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company="GRANDVIEW C-4") \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    else:
        teacher_summary_data = SessionRow.query \
            .filter_by(district_or_company=district) \
            .filter(SessionRow.status == "Completed") \
            .filter(SessionRow.date.between(start_date, end_date)) \
            .group_by(SessionRow.name, SessionRow.school, SessionRow.district_or_company) \
            .with_entities(
                SessionRow.name,
                SessionRow.school,
                SessionRow.district_or_company.label('district'),  # Assuming 'district_or_company' is the field for district
                func.count(SessionRow.id).label('total_sessions')
            ) \
            .all()
    return render_template("teacher_summary.html", teacher_summary_data=teacher_summary_data)

@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = SessionRow.query.filter_by(status=status_filter).all()
    else:
        sessions_data = SessionRow.query.all()
    return render_template("sessions.html", sessions=sessions_data)
    # return render_template("index.html")

@app.route("/session_page", methods=["GET"])
def sessions_page():
    sessions = Session.query.all()
    return render_template("session_page.html", sessions=sessions)

@app.route("/sessions_list")
def sessions_list():
    sessions = Session.query.all()
    return render_template("partials/sessions_list.html", sessions=sessions)

@app.route('/add-session', methods=['POST'])
def add_session():
    # Get form data
    session_date_str = request.form.get('sessionDate')
    session_time_str = request.form.get('sessionTime')
    session_school_name = request.form.get('sessionSchool')  # This should ideally be an identifier like an ID
    session_title = request.form.get('sessionTitle')

     # Convert date and time strings to datetime objects
    session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()  # Adjust the format if needed
    session_time = datetime.strptime(session_time_str, '%H:%M').time()  # Adjust the format if needed

    # Find or create the School entity
    school = School.query.filter_by(name=session_school_name).first()  # Assuming you are searching by name
    if not school:
        # If the school doesn't exist, create a new one (optional)
        school = School(name=session_school_name)
        db.session.add(school)
        db.session.commit()

    # Create a new session object and add to the database
    new_session = Session(title=session_title, date=session_date, start_time=session_time)
    # new_session.schools.append(school)  # Add the school to the session
    db.session.add(new_session)
    db.session.commit()

    # Redirect to the 'sessions_page' or return an appropriate response
    # return redirect(url_for('sessions_page'))
    return "<script>$('#addSessionModal').modal('hide');</script>"


@app.route('/edit-session', methods=['GET'])
def edit_session():
    session_id = request.args.get('session_id')
    session = SessionRow.query.filter_by(session_id=session_id).first()
    if session:
        return render_template('edit_session_form.html', session=session)
    else:
        return 'Session not found', 404

@app.route('/delete-session', methods=['DELETE'])
def delete_session():
    session_id = request.args.get('session_id')
    session = SessionRow.query.filter_by(session_id=session_id).first()
    if session:
        db.SessionRow.delete(session)
        db.SessionRow.commit()
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
    session = SessionRow.query.filter_by(session_id=session_id).first()
    try:
        if session:
            # Update session with the new data
            SessionRow.title = request.form['title']
            SessionRow.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            SessionRow.status = request.form['status']
            SessionRow.school = request.form['school']
            SessionRow.district_or_company = request.form['district_or_company']
            # Commit the changes to the database
            db.SessionRow.commit()
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
    subquery = SessionRow.query \
        .with_entities(SessionRow.session_id, func.min(SessionRow.id).label('min_id')) \
        .filter(SessionRow.date >= start_date, SessionRow.date <= end_date) \
        .filter(SessionRow.date >= one_year_ago) \
        .group_by(SessionRow.session_id) \
        .subquery()

    # Main query that joins the subquery
    main_query = SessionRow.query \
        .join(subquery, SessionRow.session_id == subquery.c.session_id) \
        .filter(SessionRow.id == subquery.c.min_id)

    if upcoming == 'confirmed':
        main_query = main_query.filter(SessionRow.status == 'Confirmed')
    elif upcoming == 'request':
        main_query = main_query.filter(SessionRow.status == 'Requested')

    # Apply sorting to the main query
    if sort_direction == 'asc':
        main_query = main_query.order_by(getattr(SessionRow, sort_column).asc())
    else:
        main_query = main_query.order_by(getattr(SessionRow, sort_column).desc())

    sessions_data = main_query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    one_year_ago = datetime.now() - timedelta(days=365)
    status_filter = request.args.get('statusFilter')

    # Subquery to select distinct session IDs with the earliest record based on ID
    subquery = SessionRow.query \
        .with_entities(SessionRow.session_id, func.min(SessionRow.id).label('min_id')) \
        .filter(SessionRow.date >= one_year_ago) \
        .group_by(SessionRow.session_id) \
        .subquery()

    # Main query that joins the subquery
    main_query = SessionRow.query \
        .join(subquery, SessionRow.session_id == subquery.c.session_id) \
        .filter(SessionRow.id == subquery.c.min_id)

    # Apply status filter to the main query if a filter is provided
    if status_filter:
        main_query = main_query.filter(SessionRow.status.ilike(f"%{status_filter}%"))

    sessions_data = main_query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route('/get-sessions-by-month')
def monthly_breakdown():
    # Get the selected year from query parameters, default to current year if not specified
    year = request.args.get('year', default=2023, type=int)

    start_year = str(year)  # The starting year of the academic year
    end_year = str(year + 1)  # The ending year of the academic year
    print(start_year, end_year)

    sessions_by_month = db.SessionRow.query(func.strftime('%m', SessionRow.date), func.count(SessionRow.id)) \
        .filter(or_(
            and_(func.strftime('%Y', SessionRow.date) == start_year, func.strftime('%m', SessionRow.date) >= '07'),
            and_(func.strftime('%Y', SessionRow.date) == end_year, func.strftime('%m', SessionRow.date) <= '06')
        )) \
        .filter(SessionRow.status == 'Confirmed') \
        .group_by(func.strftime('%m', SessionRow.date)) \
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
    status_filter = SessionRow.get('statusFilter', '')
    school_filter = SessionRow.get('schoolFilter', '')

    # Start with a base query
    query = SessionRow.query.filter(SessionRow.date >= one_year_ago, SessionRow.district_or_company.ilike("KANSAS CITY PUBLIC SCHOOL DISTRICT"))

    # Apply status filter if present
    if status_filter:
        query = query.filter(SessionRow.status.ilike(f"%{status_filter}%"))

    # Apply school filter if present
    if school_filter:
        query = query.filter(SessionRow.school.ilike(f"%{school_filter}%"))  # Adjust field name as necessary

    # Execute the query
    sessions_data = query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route("/clear-filters", methods=["GET"])
def clear_filters():
    SessionRow.pop('statusFilter', None)  # Remove the filter from the session if it exists
    SessionRow.pop('schoolFilter', None)
    return redirect(url_for('filter_kcps'))  # Redirect back to the filter page or wherever appropriate

@app.route("/session_details", methods=["GET"])
def session_details():
    session_id = request.args.get('session_id')
    session_data = SessionRow.query.filter_by(session_id=session_id).all()
    print(session_data)
    return render_template("session_details.html", sessions=session_data)