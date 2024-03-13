from flask import redirect, render_template, request, url_for
from app import app, db
from app.models import SessionRow, User, School, Session, Teacher, session_schools, Presenter
from datetime import datetime, timedelta
from flask import session
from sqlalchemy import func, or_, and_, case

def add_school_to_session(session_id, school_id):
    session = Session.query.get(session_id)
    school = School.query.get(school_id)
    
    # Assuming that the 'schools' relationship in the Session model is set up correctly
    session.schools.append(school)
    db.session.commit()

def soft_delete(self):
    self.deleted_at = datetime.utcnow()
    db.session.add(self)

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

    # Main query that joins Session to School, and School to District
    main_query = Session.query \
        .join(Session.schools) \
        .join(School.district) \
        .filter(District.name == district_name) \
        .filter(Session.date >= one_year_ago) \
        .filter(Session.status == 'Confirmed')  # Default Confirmed Status

    # Apply sorting to the main query
    if sort_direction == 'asc':
        main_query = main_query.order_by(getattr(Session, sort_column).asc())
    else:
        main_query = main_query.order_by(getattr(Session, sort_column).desc())

    #Default Confirmed Status
    main_query = main_query.filter(Session.status == 'Confirmed')

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
    district = request.args.get('district').lower()

    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    district_map = {
        "kck": "KANSAS CITY USD 500",
        "kcps": "KANSAS CITY PUBLIC SCHOOL DISTRICT",
        "center": "CENTER 58 SCHOOL DISTRICT",
        "hickman": "HICKMAN MILLS C-1",
        "grandview": "GRANDVIEW C-4"
    }
    district_name = district_map.get(district, district)

    summary_data = db.session.query(
        School.name.label('school_name'),
        School.level.label('school_level'),
        func.count(Session.id).label('total_sessions')
    ).select_from(Session) \
    .join(session_schools, Session.id == session_schools.c.session_id) \
    .join(School, session_schools.c.school_id == School.id) \
    .join(District, School.district_id == District.id) \
    .filter(
        District.name == district_name,
        Session.status == "Completed",
        Session.date.between(start_date, end_date)
    ).group_by(
        School.name, School.level
    ).order_by(School.name).all()

    return render_template("district_summary.html", summary_data=summary_data)



@app.route("/load-teacher-summary", methods=["GET"])
def load_teacher_summary():
    district = request.args.get('district').lower()  # Ensure case-insensitive matching
    start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    district_map = {
        "kck": "KANSAS CITY USD 500",
        "kcps": "KANSAS CITY PUBLIC SCHOOL DISTRICT",
        "center": "CENTER 58 SCHOOL DISTRICT",
        "hickman": "HICKMAN MILLS C-1",
        "grandview": "GRANDVIEW C-4"
    }
    district_name = district_map.get(district, district)  # Default to using the district arg if not found in the map

    teacher_summary_data = Teacher.query \
        .join(SessionTeacher, Teacher.id == SessionTeacher.teacher_id) \
        .join(Session, SessionTeacher.session_id == Session.id) \
        .join(Session.schools) \
        .join(School.district) \
        .filter(District.name == district_name) \
        .filter(Session.status == "Completed") \
        .filter(Session.date.between(start_date, end_date)) \
        .group_by(Teacher.name, Teacher.school_name, District.name) \
        .with_entities(
            Teacher.name.label('teacher_name'),
            Teacher.school_name.label('school_name'),
            District.name.label('district_name'),
            func.count(Session.id).label('total_sessions')
        ) \
        .all()

    return render_template("teacher_summary.html", teacher_summary_data=teacher_summary_data)

@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter_by(status=status_filter).all()
    else:
        sessions_data = Session.query.all()
    print(sessions_data)
    return render_template("sessions.html", sessions=sessions_data)

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
    status = "Confirmed"
    # Create a new session object and add to the database
    new_session = Session(title=session_title, date=session_date, start_time=session_time, status=status)
    # new_session.schools.append(school)  # Add the school to the session
    db.session.add(new_session)
    db.session.commit()
    print(new_session.id)
    # Redirect to the 'sessions_page' or return an appropriate response
    return redirect(url_for('sessions_list'))


@app.route('/edit-session', methods=['GET'])
def edit_session():
    session_id = request.args.get('session_id')
    session = Session.query.filter_by(id=session_id).first()
    if session:
        return render_template('edit_session_form.html', session=session)
    else:
        return 'Session not found', 404

@app.route('/delete-session', methods=['DELETE'])
def delete_session():
    session_id = request.args.get('session_id')
    print(session_id)
    session = Session.query.filter_by(id=session_id).first()
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
    session_id = request.form.get('session_id')
    # Fetch the session object using session_id
    session = Session.query.filter_by(id=session_id).first()

    if not session:
        return redirect(url_for('sessions_list'))

    try:
        # Update session with the new data
        session.title = request.form.get('title', session.title)
        if request.form.get('date'):
            session.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        session.status = request.form.get('status', session.status)

        # Handle multiple schools
        schools_input = request.form.get('schools')
        if schools_input:
            school_names = [name.strip() for name in schools_input.split(',')]
            print(school_names)
            session.schools = []  # Clear existing schools

            for school_name in school_names:
                school = School.query.filter_by(name=school_name).first()
                if not school:
                    school = School(name=school_name)
                    db.session.add(school)
                session.schools.append(school)

        # Handle multiple presenters
        presenters_input = request.form.get('presenters')
        if presenters_input:
            presenter_names = [name.strip() for name in presenters_input.split(';')]
            session.presenters = []  # Clear existing presenters

            for presenter_name in presenter_names:
                presenter = Presenter.query.filter_by(name=presenter_name).first()
                if not presenter:
                    presenter = Presenter(name=presenter_name)
                    db.session.add(presenter)
                session.presenters.append(presenter)


        db.session.commit()

        # return render_template('session_row.html', session=session)
        updated_row = render_template('session_row.html', session=session)
        
        # Script to clear the edit pane
        clear_script = "<script>document.getElementById('editPane').innerHTML = '';</script>"

        # Combine the updated row and script
        combined_response = updated_row + clear_script

        return combined_response

    except Exception as e:
        db.session.rollback()
        return redirect(url_for('edit_session', session_id=session_id))

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
    # one_year_ago = datetime.now() - timedelta(days=365)

    # # Get sorting parameters
    # sort_column = request.args.get('sort', 'date')  # Default sort column
    # sort_direction = request.args.get('direction', 'asc')  # Default sort direction
    # status = request.args.get('status', 'confirmed')

    # start_date = request.args.get('start_date', default=datetime(2023, 7, 1), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    # end_date = request.args.get('end_date', default=datetime.now(), type=lambda s: datetime.strptime(s, '%Y-%m-%d'))

    sessions = Session.query.all()

    print(sessions)  # For debugging

    return render_template("session_table.html", sessions=sessions)

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    one_year_ago = datetime.now() - timedelta(days=365)
    status_filter = request.args.get('statusFilter')

    # Subquery to select distinct session IDs with the earliest record based on ID
    subquery = Session.query \
        .with_entities(Session.id, func.min(Session.id).label('min_id')) \
        .filter(Session.date >= one_year_ago) \
        .group_by(Session.id) \
        .subquery()

    # Main query that joins the subquery
    main_query = Session.query \
        .join(subquery, Session.id == subquery.c.session_id) \
        .filter(Session.id == subquery.c.min_id)

    # Apply status filter to the main query if a filter is provided
    if status_filter:
        main_query = main_query.filter(Session.status.ilike(f"%{status_filter}%"))

    sessions_data = main_query.all()

    return render_template("session_table.html", sessions=sessions_data)

@app.route('/get-sessions-by-month')
def monthly_breakdown():
    year = request.args.get('year', default=datetime.now().year, type=int)

    # Define the start and end dates for the academic year
    start_date = datetime(year, 7, 1)  # Starting from July of the selected year
    end_date = datetime(year + 1, 6, 30)  # Ending in June of the following year

    # Query to group sessions by month and count them
    sessions_by_month = db.session.query(
        func.strftime('%m', Session.date).label('month'), 
        func.count(Session.id).label('total_sessions')
    ).filter(
        Session.date.between(start_date, end_date),
        Session.status == 'Confirmed'
    ).group_by(
        'month'
    ).all()

    # Sort the results by month, taking into account the academic year spanning two calendar years
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
    status_filter = Session.get('statusFilter', '')
    school_filter = Session.get('schoolFilter', '')

    # Start with a base query
    query = Session.query.filter(Session.date >= one_year_ago, Session.district.ilike("KANSAS CITY PUBLIC SCHOOL DISTRICT"))

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
    Session.pop('statusFilter', None)  # Remove the filter from the session if it exists
    Session.pop('schoolFilter', None)
    return redirect(url_for('filter_kcps'))  # Redirect back to the filter page or wherever appropriate

@app.route("/session_details", methods=["GET"])
def session_details():
    session_id = request.args.get('session_id')
    session_data = Session.query.filter_by(id=session_id).all()
    print(session_data)
    return render_template("session_details.html", sessions=session_data)