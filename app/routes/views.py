from flask import redirect, render_template, request, url_for
from app import app, db
from app.models import School, Session, Teacher, session_schools, Volunteer, Organization
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
    return render_template("/sessions/sessions.html")

@app.route('/volunteers')
def volunteers():
    search_query = request.args.get('search')
    query = Volunteer.query  # Base query
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(or_(
            Volunteer.job_category.like(search),
            Volunteer.skills.like(search),
            Volunteer.skills_text.like(search)
        ))

    # Use the filtered 'query' object to retrieve the list of volunteers
    volunteer_list = query.all()

    for volunteer in volunteer_list:
        # Combine and split by different delimiters, then strip whitespace
        combined_skills = volunteer.job_category.split(',') + volunteer.skills.split(',') + volunteer.skills_text.split(';')
        # Remove empty strings and strip whitespace from each skill
        combined_skills = [skill.strip() for skill in combined_skills if skill.strip()]
        # Assign the combined, cleaned list back to the volunteer object for easy access in the template
        volunteer.combined_skills = combined_skills

    return render_template('volunteers.html', volunteers=volunteer_list)

@app.route("/playground", methods=["GET"])
def playground():
    return render_template("playground.html")

@app.route("/search-teachers", methods=["GET"])
def search_teachers():
    teacher_name = request.args.get('teacherSearch')
    print(teacher_name)
    teachers = Teacher.query.filter(Teacher.name.ilike(f'%{teacher_name}%')).all()
    return render_template("/teachers/teacher_list.html", teachers=teachers)

@app.route("/search-presenters", methods=["GET"])
def search_presenters():
    presenter_name = request.args.get('presenterSearch')
    presenters = Volunteer.query.filter(Volunteer.name.ilike(f'%{presenter_name}%')).all()
    return render_template("/volunteers/presenter_list.html", presenters=presenters)

@app.route("/search-schools", methods=["GET"])
def search_schools():
    school_name = request.args.get('schoolSearch')
    schools = School.query.filter(School.name.ilike(f'%{school_name}%')).all()
    return render_template("/schools/school_list.html", schools=schools)

@app.route("/search-organizations", methods=["GET"])
def search_organizations():
    organization_name = request.args.get('organizationSearch')
    print(organization_name)
    organizations = db.session.query(Volunteer.organization).filter(Volunteer.organization.ilike(f'%{organization_name}%')).distinct().all()
    organizations = [org[0] for org in organizations if org[0]]  # Unpack and remove None
    return render_template("/organizations/organization_list.html", organizations=organizations)

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
    return render_template("/sessions/sessions.html", sessions=sessions_data)

@app.route("/get-add-session", methods=["GET"])
def get_add_session():
    return render_template("/sessions/add_session.html")

@app.route("/get-add-organization", methods=["GET"])
def get_add_organization():
    return render_template("/organizations/add_organization.html")

@app.route("/get-add-teacher", methods=["GET"])
def get_add_teacher():
    return render_template("/teachers/add_teacher.html")

@app.route("/get-add-presenter", methods=["GET"])
def get_add_presenter():
    return render_template("/volunteers/add_Volunteer.html")

@app.route("/get-add-school", methods=["GET"])
def get_add_school():
    return render_template("/schools/add_school.html")

@app.route("/load-sessions-table", methods=["GET"])
def load_sessions_table():
    sessions = Session.query.all()
    return render_template("/sessions/session_table.html", sessions=sessions)

@app.route("/load-organizations-table", methods=["GET"])
def load_organizations_table():
    organizations = Organization.query.all()
    return render_template("/organizations/organization_table.html", organizations=organizations)

@app.route("/session_page", methods=["GET"])
def sessions_page():
    sessions = Session.query.all()
    return render_template("/sessions/session_page.html", sessions=sessions)

@app.route("/organizations", methods=["GET"])
def organizations():
    organizations = Organization.query.all()
    return render_template("/organizations/organizations.html", organizations=organizations)

@app.route("/sessions_list")
def sessions_list():
    sessions = Session.query.all()
    return render_template("/sessions/session_list.html", sessions=sessions)

#Note: Need to make teacher store the school_id instead of the school name
@app.route("/add-teacher", methods=["POST"])
def add_teacher():
    teacher_name = request.form.get('teacherName')
    school_id = request.form.get('schoolId')
    teacher = Teacher(name=teacher_name)
    if school_id:
        school = School.query.get(school_id)
        if school:
            teacher.school_name = school.name
    db.session.add(teacher)
    db.session.commit()
    return "Submitted"

@app.route("/add-organization", methods=["POST"])
def add_organization():
    organization_name = request.form.get('organizationName')
    organization = Organization(name=organization_name)
    db.session.add(organization)
    db.session.commit()
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
    organization = request.form.get('presenterOrganization')  # Directly get the organization name from the form

    # Create a new Presenter instance with the form data
    presenter = Volunteer(name=name, email=email, phone=phone, organization=organization)

    # Add and commit the new presenter to the database
    db.session.add(presenter)
    db.session.commit()

    return "Submitted"

@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    status_filter = request.args.get('statusFilter', 'All')
    print(status_filter)
    if status_filter == 'All':
        sessions = Session.query.all()
    else:
        sessions = Session.query.filter_by(status=status_filter).all()

    return render_template("/sessions/session_table.html", sessions=sessions)

@app.route("/filter-sessions-by-date", methods=["GET"])
def filter_sessions_by_date():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date and end_date:
        sessions = Session.query.filter(Session.date >= start_date, Session.date <= end_date).all()
    else:
        sessions = Session.query.all()

    return render_template("/sessions/session_table.html", sessions=sessions)


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

    # Add the organizations to the session's organizations list
    organization_ids = request.form.getlist('organizationIds[]')  # Get the list of organization IDs
    for organization_id in organization_ids:
        organization = Organization.query.get(organization_id)  # Use `get` for ID lookup
        if organization:
            new_session.organizations.append(organization)

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
        return render_template('/sessions/edit_session_form.html', session=session)
    else:
        return 'Session not found', 404
    
@app.route('/edit-organization', methods=['GET'])
def edit_organization():
    organization_id = request.args.get('organization_id')
    organization = Organization.query.filter_by(id=organization_id).first()
    if organization:
        return render_template('/organizations/edit_organization.html', organization=organization)
    else:
        return 'Organization not found', 404

@app.route('/edit-teacher', methods=['GET'])
def edit_teacher():
    teacher_id = request.args.get('teacher_id')
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher:
        return render_template('/teachers/edit_teacher.html', teacher=teacher)
    else:
        return 'Teacher not found', 404
    
@app.route('/edit-presenter', methods=['GET'])
def edit_presenter():
    presenter_id = request.args.get('presenter_id')
    presenter = Volunteer.query.filter_by(id=presenter_id).first()
    if presenter:
        return render_template('/volunteers/edit_Volunteer.html', presenter=presenter)
    else:
        return 'Presenter not found', 404
    
@app.route('/edit-school', methods=['GET'])
def edit_school():
    school_id = request.args.get('school_id')
    school = School.query.filter_by(id=school_id).first()
    if school:
        return render_template('/schools/edit_school.html', school=school)
    else:
        return 'School not found', 404

@app.route("/update-teacher", methods=["POST"])
def update_teacher():
    teacher_id = request.form.get('teacher_id')
    teacher_name = request.form.get('teacherName')
    school_id = request.form.get('schoolId')

    # Fetch the teacher object by ID
    teacher = Teacher.query.get(teacher_id)

    if not teacher:
        # Handle the case where the teacher does not exist
        return "Teacher not found", 404

    # Update the teacher's attributes
    teacher.name = teacher_name
    if school_id:
        school = School.query.get(school_id)
        if school:
            teacher.school_name = school.name
    # Commit the changes to the database
    db.session.commit()

    # Redirect to the teachers list or return a success message
    return redirect(url_for('teachers'))

@app.route('/update-presenter', methods=['POST'])
def update_presenter():
    presenter_id = request.form.get('presenter_id')
    name = request.form.get('presenterName')
    email = request.form.get('presenterEmail')
    phone = request.form.get('presenterPhone')
    organization = request.form.get('presenterOrganization')

    presenter = Volunteer.query.get(presenter_id)
    if not presenter:
        return "Presenter not found", 404

    Volunteer.name = name
    Volunteer.email = email
    Volunteer.phone = phone
    Volunteer.organization = organization

    db.session.commit()

    return redirect(url_for('presenters'))

@app.route('/update-organization', methods=['POST'])
def update_organization():
    organization_id = request.form.get('organization_id')
    name = request.form.get('organizationName')
    email = request.form.get('organizationEmail')
    phone = request.form.get('organizationPhone')
    address = request.form.get('organizationAddress')

    organization = Organization.query.get(organization_id)
    if not organization:
        return "Organization not found", 404

    organization.name = name
    organization.email = email
    organization.phone = phone
    organization.address = address

    db.session.commit()

    return redirect(url_for('organizations'))

@app.route('/update-school', methods=['POST'])
def update_school():
    school_id = request.form.get('school_id')
    name = request.form.get('schoolName')
    state = request.form.get('schoolState')
    level = request.form.get('schoolLevel')

    school = School.query.get(school_id)
    if not school:
        return "School not found", 404

    school.name = name
    school.state = state
    school.level = level

    db.session.commit()

    return redirect(url_for('schools'))


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
    
@app.route('/delete-organization', methods=['DELETE'])
def delete_organization():
    organization_id = request.args.get('organization_id')
    organization = Organization.query.filter_by(id=organization_id).first()
    if organization:
        db.session.delete(organization)
        db.session.commit()
        return '', 200

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
    presenter = Volunteer.query.filter_by(id=presenter_id).first()
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
        session.presenters = [Volunteer.query.get(presenter_id) for presenter_id in presenter_ids if Volunteer.query.get(presenter_id)]

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
    return render_template("/teachers/teachers.html")

@app.route("/load-teacher-table", methods=["GET"])
def load_teacher_table():
    teachers = Teacher.query.all()
    return render_template("/teachers/teacher_table.html", teachers=teachers)

@app.route("/schools", methods=["GET"])
def schools():
    return render_template("/schools/schools.html")

@app.route("/load-school-table", methods=["GET"])
def load_school_table():
    schools = School.query.all()
    return render_template("/schools/school_table.html", schools=schools)

@app.route("/presenters", methods=["GET"])
def presenters():
    return render_template("/volunteers/presenters.html")

@app.route("/load-presenter-table", methods=["GET"])
def load_presenter_table():
    presenters = Volunteer.query.all()
    return render_template("/volunteers/presenter_table.html", presenters=presenters)