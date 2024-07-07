from flask import flash, redirect, render_template, request, url_for
from app import app, db
from app.models import School, Session, Teacher, session_schools, Volunteer, Organization
from datetime import datetime, timedelta
from flask import session
from sqlalchemy import func, or_, and_, case
from flask import jsonify
from app.templates.sessions.partials.session_types import session_types

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

@app.route("/playground", methods=["GET"])
def playground():
    return render_template("playground.html")

@app.route("/search-teachers", methods=["GET"])
def search_teachers():
    teacher_name = request.args.get('teacherSearch')
    teachers = Teacher.query.filter(Teacher.name.ilike(f'%{teacher_name}%')).all()
    return render_template("/teachers/teacher_list.html", teachers=teachers)

@app.route("/search-volunteers", methods=["GET"])
def search_volunteers():
    volunteer_name = request.args.get('volunteerSearch')
    volunteers = Volunteer.query.filter(Volunteer.name.ilike(f'%{volunteer_name}%')).all()
    return render_template("/volunteers/volunteer_list.html", volunteers=volunteers)

@app.route("/search-schools", methods=["GET"])
def search_schools():
    school_name = request.args.get('schoolSearch')
    schools = School.query.filter(School.name.ilike(f'%{school_name}%')).all()
    return render_template("/schools/school_list.html", schools=schools)

@app.route("/search-organizations", methods=["GET"])
def search_organizations():
    organization_name = request.args.get('organizationSearch')
    organizations = db.session.query(Organization).filter(Organization.name.ilike(f'%{organization_name}%')).distinct().all()
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

@app.route("/add-session", methods=["GET"])
def get_add_session():
    return render_template('/sessions/add_session.html', session_types=session_types)

@app.route("/get-add-organization", methods=["GET"])
def get_add_organization():
    return render_template("/organizations/add_organization.html")

@app.route("/add-teacher", methods=["GET"])
def get_add_teacher():
    return render_template("/teachers/add_teacher.html")

@app.route("/add-volunteer", methods=["GET"])
def get_add_volunteer():
    return render_template("/volunteers/add_volunteer.html")

@app.route("/add-school", methods=["GET"])
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
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    school_id = request.form.get('schoolId')
    teacher = Teacher(first_name=first_name, last_name=last_name, email=email, primary_affiliation_id=school_id, type='Teacher')  # Assuming 'type' is required
    db.session.add(teacher)
    db.session.commit()
    return redirect(url_for('teachers'))

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
    district = request.form.get('schoolDistrict')
    level = request.form.get('schoolLevel')
    school = School(name=name, district=district, level=level)
    db.session.add(school)
    db.session.commit()
    return redirect(url_for('schools'))

@app.route("/add-volunteer", methods=["POST"])
def add_volunteer():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    organization_id = request.form.get('organizationId')
    volunteer = Volunteer(first_name=first_name, last_name=last_name, email=email, primary_affiliation_id=organization_id)
    db.session.add(volunteer)
    db.session.commit()
    return redirect(url_for('volunteers'))

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

@app.route('/session_details/<int:session_id>')
def session_details(session_id):
    session = Session.query.get_or_404(session_id)
    return render_template('/sessions/session_details.html', session=session)

@app.route('/clear-details-pane')
def clear_details_pane():
    return '<div id="detailsPane"></div>'


@app.route('/add-session', methods=['POST'])
def add_session():
    # Get form data
    session_date_str = request.form.get('sessionDate')
    session_time_str = request.form.get('sessionTime')
    end_time_str = request.form.get('sessionEndTime')
    session_title = request.form.get('sessionTitle')
    session_status = request.form.get('sessionStatus')
    session_type = request.form.get('sessionType')
    session_topic = request.form.get('sessionTopic')

    # Convert date and time strings to datetime objects
    session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()
    session_time = datetime.strptime(session_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()

    # Create a new session object with default values
    new_session = Session(
        start_date=session_date,
        start_time=session_time,
        end_time=end_time,
        name=session_title,
        status=session_status,
        type=session_type,
        topic=session_topic,
        manual_student_count=0,  # Set default student count
        skills_needed=None,  # Assuming skills_needed can be nullable
    )

    # Optionally add teachers to the session's teachers list
    teacher_ids = request.form.getlist('teacherIds[]')
    for teacher_id in teacher_ids:
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            new_session.teachers.append(teacher)

    # Optionally add volunteers to the session's volunteers list
    volunteer_ids = request.form.getlist('volunteerIds[]')
    for volunteer_id in volunteer_ids:
        volunteer = Volunteer.query.get(volunteer_id)
        if volunteer:
            new_session.volunteers.append(volunteer)

    # Add the new session to the DB session and commit
    db.session.add(new_session)
    db.session.commit()

    # Redirect or return a response
    return redirect(url_for('sessions'))

@app.route('/edit-session/<int:session_id>', methods=['GET', 'POST'])
def edit_session(session_id):
    session = Session.query.get_or_404(session_id)
    if request.method == 'POST':
        session.name = request.form.get('sessionTitle')
        session.start_date = datetime.strptime(request.form.get('sessionDate'), '%Y-%m-%d').date()
        session.start_time = datetime.strptime(request.form.get('sessionTime'), '%H:%M').time()
        session.end_time = datetime.strptime(request.form.get('sessionEndTime'), '%H:%M').time()
        session.status = request.form.get('sessionStatus')
        session.type = request.form.get('sessionType')
        session.manual_student_count = request.form.get('manualStudentCount')
        session.pathway = request.form.get('pathway')
        session.skills_needed = request.form.get('skillsNeeded')
        session.topic = request.form.get('sessionTopic')

        db.session.commit()

        return redirect(url_for('sessions'))

    return render_template('/sessions/edit_session_form.html', session=session, session_types=session_types)

    
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
        return render_template('/teachers/edit_teacher.html', teacher=teacher, person=teacher)
    else:
        return 'Teacher not found', 404
    
@app.route('/edit-volunteer', methods=['GET'])
def edit_volunteer():
    volunteer_id = request.args.get('volunteer_id')
    volunteer = Volunteer.query.filter_by(id=volunteer_id).first()
    if volunteer:
        return render_template('/volunteers/edit_Volunteer.html', volunteer=volunteer, person=volunteer)
    else:
        return 'volunteer not found', 404
    
@app.route('/edit-school', methods=['GET'])
def edit_school():
    school_id = request.args.get('school_id')
    school = School.query.filter_by(id=school_id).first()
    if school:
        return render_template('/schools/edit_school.html', school=school)
    else:
        return 'School not found', 404

def update_person_data(person, form):
    person.first_name = form.get('firstName')
    person.last_name = form.get('lastName')
    person.middle_name = form.get('middleName')
    person.suffix = form.get('suffix')
    person.email = form.get('email')
    person.address = form.get('address')
    person.primary_phone = form.get('primaryPhone')
    person.secondary_phone = form.get('secondaryPhone')
    person.active = form.get('active') == 'true'
    person.birthday = datetime.strptime(form.get('birthday'), '%Y-%m-%d').date() if form.get('birthday') else None
    person.connector_account_id = form.get('connectorAccountId')
    person.gender = form.get('gender')
    person.contact_type = form.get('contactType')

@app.route("/update-teacher/<int:teacher_id>", methods=["POST"])
def update_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    update_person_data(teacher, request.form)

    # Teacher fields
    teacher.primary_affiliation_id = request.form.get('schoolId')
    teacher.type = request.form.get('type')

    db.session.commit()

    return redirect(url_for('teachers'))

@app.route('/update-volunteer/<int:volunteer_id>', methods=['POST'])
def update_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    update_person_data(volunteer, request.form)

    # Volunteer fields
    volunteer.title = request.form.get('title')
    volunteer.primary_affiliation_id = request.form.get('organizationId')
    volunteer.education_background = request.form.get('educationBackground')
    volunteer.last_mailchimp_email_date = datetime.strptime(request.form.get('lastMailchimpEmailDate'), '%Y-%m-%dT%H:%M:%S') if request.form.get('lastMailchimpEmailDate') else None
    volunteer.last_volunteer_date = datetime.strptime(request.form.get('lastVolunteerDate'), '%Y-%m-%dT%H:%M:%S') if request.form.get('lastVolunteerDate') else None

    db.session.commit()

    return redirect(url_for('volunteers'))

@app.route('/update-organization/<int:organization_id>', methods=['POST'])
def update_organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    organization.name = request.form.get('organizationName')
    db.session.commit()

    return redirect(url_for('organizations'))

@app.route('/update-school/<int:school_id>', methods=['POST'])
def update_school(school_id):
    school = School.query.get_or_404(school_id)
    school.name = request.form.get('schoolName')
    school.district = request.form.get('schoolDistrict')
    school.level = request.form.get('schoolLevel')
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
    
@app.route('/delete-volunteer', methods=['DELETE'])
def delete_volunteer():
    volunteer_id = request.args.get('volunteer_id')
    volunteer = Volunteer.query.filter_by(id=volunteer_id).first()
    if volunteer:
        db.session.delete(volunteer)
        db.session.commit()
        return '', 200

@app.route('/clear-edit-pane', methods=['GET'])
def clear_edit_pane():
    return '<div id="editPane" class="edit-pane"></div>'  # Returns an empty response to clear the pane

# @app.route('/update-session', methods=['POST'])
# def update_session():
#     session_id = request.form.get('session_id')
#     session = Session.query.filter_by(id=session_id).first()

#     if not session:
#         return redirect(url_for('sessions_list'))

#     try:
#         session.title = request.form.get('title', session.title)
#         session.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d') if request.form.get('date') else session.date
#         session.status = request.form.get('status', session.status)

#         teacher_ids = request.form.getlist('teacherIds[]')
#         session.teachers = [Teacher.query.get(teacher_id) for teacher_id in teacher_ids if Teacher.query.get(teacher_id)]

#         volunteer_ids = request.form.getlist('volunteerIds[]')
#         session.volunteers = [Volunteer.query.get(volunteer_id) for volunteer_id in volunteer_ids if Volunteer.query.get(volunteer_id)]

#         db.session.commit()
        
#         updated_row = render_template('/sessions/session_row.html', session=session)
        
#         # Script to clear the edit pane
#         clear_script = "<script>document.getElementById('editPane').innerHTML = '';</script>"

#         # Combine the updated row and script
#         combined_response = updated_row + clear_script

#         return combined_response

#     except Exception as e:
#         db.session.rollback()
#         return redirect(url_for('edit_session', session_id=session_id))

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

@app.route("/volunteers", methods=["GET"])
def volunteers():
    return render_template("/volunteers/volunteers.html")

@app.route("/load-volunteer-table", methods=["GET"])
def load_volunteer_table():
    volunteers = Volunteer.query.all()
    return render_template("/volunteers/volunteer_table.html", volunteers=volunteers)