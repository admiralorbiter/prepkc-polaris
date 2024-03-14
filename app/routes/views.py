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

@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')
    if status_filter:
        sessions_data = Session.query.filter_by(status=status_filter).all()
    else:
        sessions_data = Session.query.all()
    print(sessions_data)
    return render_template("sessions.html", sessions=sessions_data)

@app.route("/load-sessions-table", methods=["GET"])
def load_sessions_table():
    sessions = Session.query.all()
    return render_template("session_table.html", sessions=sessions)

@app.route("/session_page", methods=["GET"])
def sessions_page():
    sessions = Session.query.all()
    return render_template("session_page.html", sessions=sessions)

@app.route("/sessions_list")
def sessions_list():
    sessions = Session.query.all()
    return render_template("/partials/session_list.html", sessions=sessions)

@app.route("/add-teacher", methods=["POST"])
def add_teacher():
    teacher_name = request.form.get('teacherName')
    school_name = request.form.get('schoolName')
    teacher = Teacher(name=teacher_name, school_name=school_name)
    db.session.add(teacher)
    db.session.commit()
    print(teacher.id)
    print(teacher.school_name)
    return "Submitted"

@app.route('/add-session', methods=['POST'])
def add_session():
    # Get form data
    session_date_str = request.form.get('sessionDate')
    session_time_str = request.form.get('sessionTime')
    session_school_name = request.form.get('sessionSchool')  # This should ideally be an identifier like an ID
    session_title = request.form.get('sessionTitle')
    session_presenter = request.form.get('sessionPresenter')
    session_organization = request.form.get('sessionOrganization')

     # Convert date and time strings to datetime objects
    session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()  # Adjust the format if needed
    session_time = datetime.strptime(session_time_str, '%H:%M').time()  # Adjust the format if needed

   # Find or create the School entity
    school = School.query.filter_by(name=session_school_name).first()
    if not school:
        school = School(name=session_school_name)
        db.session.add(school)
        # Don't commit yet, as we might need to roll back if something fails later

    # Find or create the Presenter entity
    presenter = Presenter.query.filter_by(name=session_presenter).first()
    if not presenter:
        presenter = Presenter(name=session_presenter, organization=session_organization)
        db.session.add(presenter)
        # Don't commit yet for the same reason as above
    status="Pending"
    # Create a new session object
    new_session = Session(title=session_title, date=session_date, start_time=session_time, status=status)
    
    # Associate the school and presenter with the session
    new_session.schools.append(school)  # Assuming 'schools' is a many-to-many relationship
    new_session.presenters.append(presenter)  # Assuming 'presenters' is a one-to-many relationship

    db.session.add(new_session)
    db.session.commit()  # Now commit everything including the associations

    # Redirect or return a response
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

@app.route("/teachers", methods=["GET"])
def teachers():
    return render_template("teachers.html")

@app.route("/load-teacher-table", methods=["GET"])
def load_teacher_table():
    teachers = Teacher.query.all()
    return render_template("/tables/teacher_table.html", teachers=teachers)

@app.route("/schools", methods=["GET"])
def schools():
    return render_template("schools.html")

@app.route("/load-school-table", methods=["GET"])
def load_school_table():
    schools = School.query.all()
    return render_template("/tables/school_table.html", schools=schools)

@app.route("/presenters", methods=["GET"])
def presenters():
    return render_template("presenters.html")

@app.route("/load-presenter-table", methods=["GET"])
def load_presenter_table():
    presenters = Presenter.query.all()
    return render_template("/tables/presenter_table.html", presenters=presenters)