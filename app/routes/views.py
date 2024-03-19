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

@app.route("/playground", methods=["GET"])
def playground():
    return render_template("playground.html")

@app.route("/search-teachers", methods=["GET"])
def search_teachers():
    teacher_name = request.args.get('teacherSearch')
    print(teacher_name)
    teachers = Teacher.query.filter(Teacher.name.ilike(f'%{teacher_name}%')).all()
    return render_template("/partials/teacher_list.html", teachers=teachers)

@app.route("/search-presenters", methods=["GET"])
def search_presenters():
    presenter_name = request.args.get('presenterSearch')
    presenters = Presenter.query.filter(Presenter.name.ilike(f'%{presenter_name}%')).all()
    return render_template("/partials/presenter_list.html", presenters=presenters)

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

@app.route("/get-add-session", methods=["GET"])
def get_add_session():
    return render_template("/modals/add_session.html")

@app.route("/load-sessions-table", methods=["GET"])
def load_sessions_table():
    sessions = Session.query.all()
    return render_template("/tables/session_table.html", sessions=sessions)

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

@app.route("/add-school", methods=["POST"])
def add_school():
    name = request.form.get('schoolName')
    state = request.form.get('schoolState')
    level = request.form.get('schoolLevel')
    school = School(name=name, state=state, level=level)
    db.session.add(school)
    db.session.commit()
    return "Submitted"

@app.route("/add-presenter", methods=["POST"])
def add_presenter():
    name = request.form.get('presenterName')
    email = request.form.get('presenterEmail')
    phone = request.form.get('presenterPhone')
    organization = request.form.get('presenterOrganization')
    presenter = Presenter(name=name, email=email, phone=phone, organization=organization)
    db.session.add(presenter)
    db.session.commit()
    return "Submitted"
    
@app.route('/add-session', methods=['POST'])
def add_session():
    # Get form data
    session_date_str = request.form.get('sessionDate')
    session_time_str = request.form.get('sessionTime')
    session_title = request.form.get('sessionTitle')

    # Convert date and time strings to datetime objects
    session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()  # Adjust the format if needed
    session_time = datetime.strptime(session_time_str, '%H:%M').time()  # Adjust the format if needed

    # Create a new session object
    new_session = Session(date=session_date, start_time=session_time, title=session_title, status="Pending")
    
    # Add the teacher to the session's teachers list
    teacher_ids = request.form.getlist('teacherIds[]')  # Get the list of teacher IDs
    for teacher_id in teacher_ids:
        teacher = Teacher.query.get(teacher_id)  # Use `get` for ID lookup
        if teacher:
            new_session.teachers.append(teacher)

    # Add the new session to the DB session and commit
    db.session.add(new_session)
    db.session.commit()

    # Redirect or return a response
    return redirect(url_for('sessions_list'))



@app.route('/edit-session', methods=['GET'])
def edit_session():
    session_id = request.args.get('session_id')
    session = Session.query.filter_by(id=session_id).first()
    if session:
        return render_template('/forms/edit_session_form.html', session=session)
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
    
@app.route('/delete-school', methods=['DELETE'])
def delete_school():
    school_id = request.args.get('school_id')
    school = School.query.filter_by(id=school_id).first()
    if school:
        db.session.delete(school)
        db.session.commit()
        return '', 200
    
@app.route('/delete-teacher', methods=['DELETE'])
def delete_teacher():
    teacher_id = request.args.get('teacher_id')
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return '', 200
    
@app.route('/delete-presenter', methods=['DELETE'])
def delete_presenter():
    presenter_id = request.args.get('presenter_id')
    presenter = Presenter.query.filter_by(id=presenter_id).first()
    if presenter:
        db.session.delete(presenter)
        db.session.commit()
        return '', 200

@app.route('/clear-edit-pane', methods=['GET'])
def clear_edit_pane():
    return '<div id="editPane" class="edit-pane"></div>'  # Returns an empty response to clear the pane

@app.route('/update-session', methods=['POST'])
def update_session():
    session_id = request.form.get('session_id')
    session = Session.query.filter_by(id=session_id).first()

    if not session:
        return redirect(url_for('sessions_list'))

    try:
        session.title = request.form.get('title', session.title)
        session.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d') if request.form.get('date') else session.date
        session.status = request.form.get('status', session.status)

        teacher_ids = request.form.getlist('teacherIds[]')
        session.teachers = [Teacher.query.get(teacher_id) for teacher_id in teacher_ids if Teacher.query.get(teacher_id)]

        presenter_ids = request.form.getlist('presenterIds[]')
        session.presenters = [Presenter.query.get(presenter_id) for presenter_id in presenter_ids if Presenter.query.get(presenter_id)]

        db.session.commit()
        
        updated_row = render_template('/tables/session_row.html', session=session)
        
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