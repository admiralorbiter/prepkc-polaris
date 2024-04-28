from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Session, Teacher, Presenter, School

app = Blueprint('app_routes', __name__)

##[Defaut Route] Index
# This route is used to render the index page of the application.
# The index page contains the first page of the application with a brief description of the application and a link to the sessions page.
@app.route('/')
def index():
    return render_template('index.html')

##[Helper Function] Prepare Sessions
# This function is used to prepare the session data before rendering it on the sessions page.
# Note Slightly slower than formatting it directly on the front end, but with pagination there should be no noticeable difference.
def prepare_sessions(sessions):
# Documentation Example:
# Prepare session data for rendering on the sessions page.

# This function formats session details, including dates, times, and associated names from various
# related entities like schools, teachers, and presenters. It ensures that if certain data is
# not set, default messages are displayed instead. This is particularly useful to handle cases
# where session information might be incomplete.

# Although this method may be slightly slower than formatting directly on the front-end, 
# the difference is usually negligible, especially when pagination is used to limit the number 
# of sessions processed at one time.

# Args:
# sessions (list of Session objects): A list of session objects, each potentially containing
#                                     attributes like date, start_time, teachers, and presenters.

# Returns:
# list of Session objects: The same list of session objects, but with additional attributes set
#                             for formatted date, time, school names, teacher names, presenter names,
#                             and presenter organizations.

# Example of additional attributes added to each session object:
# - formatted_date: String, formatted date ('mm/dd/yyyy') or 'Date not set'
# - formatted_time: String, formatted time ('HH:MM') or 'Time not set'
# - school_names: String, comma-separated school names or 'No schools'
# - teacher_names: String, comma-separated teacher names or 'Teachers not set'
# - presenter_names: String, comma-separated presenter names or 'Presenters not set'
# - presenter_orgs: String, comma-separated presenter organizations or 'No organizations'

    # Loop through each session and format the date, time, school names, teacher names, and presenter names.
    # If Data is not set, it will display a default message.
    for session in sessions:
        session.formatted_date = session.date.strftime('%m/%d/%Y') if session.date else 'Date not set'
        session.formatted_time = session.start_time.strftime('%H:%M') if session.start_time else 'Time not set'

        # Ensure unique school names using a set by using a loop to add each school name to the set.
        unique_schools = set()
        for teacher in session.teachers:
            unique_schools.add(teacher.school_name)

        session.school_names = ', '.join(unique_schools) if session.teachers else 'No schools'
        session.teacher_names = ', '.join(teacher.name for teacher in session.teachers) if session.teachers else 'Teachers not set'
        session.presenter_names = ', '.join(presenter.name for presenter in session.presenters) if session.presenters else 'Presenters not set'
        session.presenter_orgs = ', '.join(presenter.organization for presenter in session.presenters) if session.presenters else 'No organizations'
    return sessions

##[Session Route] Sessions
# This route is used to display the sessions page. It fetches all the sessions from the database and prepares the data before rendering it on the page.
# It also accepts a query parameter `statusFilter` to filter the sessions based on their status. Then it prepares the data and renders the sessions page.
@app.route("/sessions", methods=["GET"])
def sessions():
    status_filter = request.args.get('statusFilter')                            # Get the status filter from the query parameters
    if status_filter:                                                           # Check if the status filter is present        
        sessions_data = Session.query.filter_by(status=status_filter).all()     # Filter the sessions based on the status
    else:                                                                       # Else
        sessions_data = Session.query.all()                                         # Get all the sessions if no filter is applied
    sessions_data = prepare_sessions(sessions_data)                                 # Prepare the session data
    return render_template("sessions.html", sessions=sessions_data)                 # Render the sessions page with the session data

##[Presenter Route] Presenters
# This route is used to display the presenters page. It fetches all the presenters from the database and renders the presenters page.
@app.route("/presenters", methods=["GET"])
def presenters():
    presenters = Presenter.query.all()                                          # Get all the presenters
    return render_template("presenters.html", presenters=presenters)            # Render the presenters page with the presenter data

##[Teacher Route] Teachers
# This route is used to display the teachers page. It fetches all the teachers from the database and renders the teachers page.
@app.route("/teachers", methods=["GET"])
def teachers():
    teachers = Teacher.query.all()                                              # Get all the teachers
    return render_template("teachers.html", teachers=teachers)                  # Render the teachers page with the teacher data

##[School Route] Schools
# This route is used to display the schools page. It fetches all the schools from the database and renders the schools page.
@app.route("/schools", methods=["GET"])
def schools():
    schools = School.query.all()                                                # Get all the schools
    return render_template("schools.html", schools=schools)                    # Render the schools page with the school data

##[Session Route] Delete Session
# This route is used to delete a session based on the session ID provided in the query parameters.
@app.route('/delete-session', methods=['DELETE'])
def delete_session():
    session_id = request.args.get('session_id')                                 # Get the session ID from the query parameters
    session = Session.query.filter_by(id=session_id).first()                    # Find the session based on the session ID
    if session:                                                                 # If Session Exists
        db.session.delete(session)                                                  # Delete the session
        db.session.commit()                                                         # Commit the changes
        return '', 200                                                              # Return an empty response with a 200 OK status when successfully deleted
    else:                                                                       # Else                     
        return 'Session not found', 404                                             # Return a 404 if the session doesn't exist
    
##[Presenter Route] Delete Presenter
# This route is used to delete a presenter based on the presenter ID provided in the query parameters.
@app.route('/delete-presenter', methods=['DELETE'])
def delete_presenter():
    presenter_id = request.args.get('presenter_id')                             # Get the presenter ID from the query parameters
    presenter = Presenter.query.filter_by(id=presenter_id).first()              # Find the presenter based on the presenter ID
    if presenter:                                                               # If Presenter Exists
        db.session.delete(presenter)                                                # Delete the presenter
        db.session.commit()                                                         # Commit the changes
        return '', 200                                                              # Return an empty response with a 200 OK status when successfully deleted
    else:                                                                       # Else
        return 'Presenter not found', 404                                           # Return a 404 if the presenter doesn't exist

##[Teacher Route] Delete Teacher
# This route is used to delete a teacher based on the teacher ID provided in the query parameters.
@app.route('/delete-teacher', methods=['DELETE'])
def delete_teacher():
    teacher_id = request.args.get('teacher_id')                                 # Get the teacher ID from the query parameters
    teacher = Teacher.query.filter_by(id=teacher_id).first()                    # Find the teacher based on the teacher ID
    if teacher:                                                                 # If Teacher Exists
        db.session.delete(teacher)                                                  # Delete the teacher
        db.session.commit()                                                         # Commit the changes
        return '', 200                                                              # Return an empty response with a 200 OK status when successfully deleted
    else:                                                                       # Else
        return 'Teacher not found', 404                                             # Return a 404 if the teacher doesn't exist
    
##[School Route] Delete School
# This route is used to delete a school based on the school ID provided in the query parameters.
@app.route('/delete-school', methods=['DELETE'])
def delete_school():
    school_id = request.args.get('school_id')                                   # Get the school ID from the query parameters
    school = School.query.filter_by(id=school_id).first()                       # Find the school based on the school ID
    if school:                                                                  # If School Exists
        db.session.delete(school)                                                   # Delete the school
        db.session.commit()                                                         # Commit the changes
        return '', 200                                                              # Return an empty response with a 200 OK status when successfully deleted
    else:                                                                       # Else
        return 'School not found', 404                                              # Return a 404 if the school doesn't exist

##[Session Route] Filter Sessions by Status
# This route is used to filter the sessions based on the status filter provided in the query parameters.
@app.route("/filter-sessions", methods=["GET"])
def filter_sessions():
    status_filter = request.args.get('statusFilter', 'All')                     # Get the status filter from the query parameters, default to 'All'
    if status_filter == 'All':                                                  # If the status filter is 'All'
        sessions = Session.query.all()                                              # Get all the sessions
    else:                                                                       # Else
        sessions = Session.query.filter_by(status=status_filter).all()              # Filter the sessions based on the status
    sessions = prepare_sessions(sessions)                                       # Prepare the session data
    return render_template("/tables/sessions.html", sessions=sessions, current_filter=status_filter)

##[Session Route] Filter Sessions by Date
# This route is used to filter the sessions based on the date range provided in the query parameters.
@app.route("/filter-sessions-by-date", methods=["GET"])
def filter_sessions_by_date():
    start_date = request.args.get('start_date')                                 # Get the start date from the query parameters
    end_date = request.args.get('end_date')                                     # Get the end date from the query parameters

    if start_date and end_date:                                                 # If both start and end dates are provided
        sessions = Session.query.filter(
            Session.date >= start_date, Session.date <= end_date).all()             # Filter the sessions based on the date range
    else:                                                                       # Else
        sessions = Session.query.all()                                              # Get all the sessions
    sessions = prepare_sessions(sessions)                                       # Prepare the session data
    return render_template("/tables/sessions.html", sessions=sessions)

##[Session Route] Edit Session
# This route is used to GET the form to  edit a session based on the session ID provided in the query parameters.
@app.route('/edit-session', methods=['GET'])
def edit_session():
    session_id = request.args.get('session_id')                                 # Get the session ID from the query parameters
    session = Session.query.filter_by(id=session_id).first()                    # Find the session based on the session ID
    if session:                                                                 # If Session Exists
        return render_template('/forms/edit_session.html', session=session)         # Render the edit session form with the session data
    else:                                                                       # Else
        return 'Session not found', 404                                         # Return a 404 if the session doesn't exist

##[Presenter Route] Edit Presenter
# This route is used to GET the form to edit a presenter based on the presenter ID provided in the query parameters.
@app.route('/edit-presenter', methods=['GET'])
def edit_presenter():
    presenter_id = request.args.get('presenter_id')                             # Get the presenter ID from the query parameters
    presenter = Presenter.query.filter_by(id=presenter_id).first()              # Find the presenter based on the presenter ID
    if presenter:                                                               # If Presenter Exists
        return render_template('/forms/edit_presenter.html', presenter=presenter)   # Render the edit presenter form with the presenter data
    else:                                                                       # Else
        return 'Presenter not found', 404                                         # Return a 404 if the presenter doesn't exist

##[Teacher Route] Edit Teacher
# This route is used to GET the form to edit a teacher based on the teacher ID provided in the query parameters.
@app.route('/edit-teacher', methods=['GET'])
def edit_teacher():
    teacher_id = request.args.get('teacher_id')                                 # Get the teacher ID from the query parameters
    teacher = Teacher.query.filter_by(id=teacher_id).first()                    # Find the teacher based on the teacher ID
    if teacher:                                                                 # If Teacher Exists
        return render_template('/forms/edit_teacher.html', teacher=teacher)         # Render the edit teacher form with the teacher data
    else:                                                                       # Else
        return 'Teacher not found', 404                                           # Return a 404 if the teacher doesn't exist
    
##[School Route] Edit School
# This route is used to GET the form to edit a school based on the school ID provided in the query parameters.
@app.route('/edit-school', methods=['GET'])
def edit_school():
    school_id = request.args.get('school_id')                                   # Get the school ID from the query parameters
    school = School.query.filter_by(id=school_id).first()                        # Find the school based on the school ID
    if school:                                                                  # If School Exists
        return render_template('/forms/edit_school.html', school=school)            # Render the edit school form with the school data
    else:                                                                       # Else
        return 'School not found', 404                                             # Return a 404 if the school doesn't exist

##[Session Route] Update Session
# This route is used to update a session based on the form data provided in the POST request.
@app.route('/update-session', methods=['POST'])
def update_session():
    session_id = request.form.get('session_id')                                 # Get the session ID from the form data
    session = Session.query.filter_by(id=session_id).first()                    # Find the session based on the session ID
    if not session:                                                             # If Session Doesn't Exist
        return redirect(url_for('app_routes.sessions'))                             # Redirect to the sessions page

    try:                    
        session.title = request.form.get('title', session.title)                                                                            # Update the session title
        session.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d') if request.form.get('date') else session.date                # Update the session date
        session.status = request.form.get('status', session.status)                                                                         # Update the session status

        teacher_ids = request.form.getlist('teacherIds[]')                                                                                  # Get the teacher IDs from the form data
        session.teachers = [Teacher.query.get(teacher_id) for teacher_id in teacher_ids if Teacher.query.get(teacher_id)]                   # Update the teachers for the session

        presenter_ids = request.form.getlist('presenterIds[]')                                                                              # Get the presenter IDs from the form data
        session.presenters = [Presenter.query.get(presenter_id) for presenter_id in presenter_ids if Presenter.query.get(presenter_id)]     # Update the presenters for the session
        db.session.commit()                                                                                                                 # Commit the changes
        return redirect(url_for('app_routes.sessions'))                                                                                     # Redirect to the sessions page

    except Exception as e:                                                      # Handle any exceptions
        db.session.rollback()                                                   # Rollback the session                                                              
        return redirect(url_for('app_routes.edit_session', session_id=session_id))
    
##[Presenter Route] Update Presenter
# This route is used to update a presenter based on the form data provided in the POST request.
@app.route('/update-presenter', methods=['POST'])
def update_presenter():
    presenter_id = request.form.get('presenter_id')                             # Get the presenter ID from the form data
    presenter = Presenter.query.filter_by(id=presenter_id).first()              # Find the presenter based on the presenter ID
    if not presenter:                                                           # If Presenter Doesn't Exist
        return redirect(url_for('app_routes.presenters'))                           # Redirect to the presenters page if presenter doesn't exist

    try:                                                                        # Try to update the presenter data
        presenter.name = request.form.get('name', presenter.name)
        presenter.email = request.form.get('email', presenter.email)
        presenter.phone = request.form.get('phone', presenter.phone)
        presenter.organization = request.form.get('organization', presenter.organization)
        presenter.local = request.form.get('local') == 'true'                   # Convert the string 'true'/'false' to boolean
        presenter.ethnicity = request.form.get('ethnicity', presenter.ethnicity)
        presenter.job_title = request.form.get('job_title', presenter.job_title)
        presenter.city = request.form.get('city', presenter.city)
        presenter.state = request.form.get('state', presenter.state)
        presenter.postal_code = request.form.get('postal_code', presenter.postal_code)
        
        db.session.commit()                                                     # Commit the changes
        return redirect(url_for('app_routes.presenters'))                       # Redirect back to the presenters page

    except Exception as e:
        db.session.rollback()                                                   # Rollback in case of any exception
        return redirect(url_for('app_routes.edit_presenter', presenter_id=presenter_id))  # Redirect back to the edit page if an error occurs
##[School Route] Update School
# This route is used to update a school based on the form data provided in the POST request.
@app.route('/update-teacher', methods=['POST'])
def update_teacher():
    teacher_id = request.form.get('teacher_id')                                 # Get the teacher ID from the form data
    teacher = Teacher.query.filter_by(id=teacher_id).first()                    # Find the teacher based on the teacher ID
    if not teacher:                                                             # If Teacher Doesn't Exist
        return redirect(url_for('app_routes.teachers'))                             # Redirect to the teachers page if teacher doesn't exist

    try:                                                                        # Update the teacher's details from the form data
        teacher.name = request.form.get('name', teacher.name)
        teacher.school_name = request.form.get('school_name', teacher.school_name)
        session_ids = request.form.getlist('sessionIds[]')                      # Get the session IDs from the form data
        if session_ids:                                                         # If session IDs are provided then update the sessions
            teacher.sessions = [Session.query.get(session_id) for session_id in session_ids if Session.query.get(session_id)]
        
        db.session.commit()                                                     # Commit the changes
        return redirect(url_for('app_routes.teachers'))                         # Redirect back to the teachers page

    except Exception as e:
        db.session.rollback()  # Rollback in case of any exception
        print(e)  # Optionally print or log the exception for debugging
        return redirect(url_for('app_routes.edit_teacher', teacher_id=teacher_id))  # Redirect back to the edit page if an error occurs

##[School Route] Update School
# This route is used to update a school based on the form data provided in the POST request.
@app.route('/update-school', methods=['POST'])
def update_school():
    school_id = request.form.get('school_id')                                   # Get the school ID from the form data
    school = School.query.filter_by(id=school_id).first()                       # Find the school based on the school ID
    if not school:                                                              # If School Doesn't Exist
        return redirect(url_for('app_routes.schools'))                              # Redirect to the schools page if school doesn't exist

    try:                                                                        # Update the school's details from the form data
        school.name = request.form.get('name', school.name)
        school.district = request.form.get('district', school.district)
        school.level = request.form.get('level', school.level)
        school.state = request.form.get('state', school.state)
        session_ids = request.form.getlist('sessionIds[]')                      # Get the session IDs from the form data
        if session_ids:                                                         # If session IDs are provided then update the sessions
            school.sessions = [Session.query.get(session_id) for session_id in session_ids if Session.query.get(session_id)]
        
        db.session.commit()                                                     # Commit the changes
        return redirect(url_for('app_routes.schools'))                          # Redirect back to the schools page

    except Exception as e:
        db.session.rollback()                                                   # Rollback in case of any exception
        return redirect(url_for('app_routes.edit_school', school_id=school_id)) # Redirect back to the edit page if an error occurs


##[Session Route] Get Add Session Form
# This route is used to GET the form to add a new session.
@app.route("/get-create-session", methods=["GET"])
def get_add_session():
    return render_template("/forms/create_session.html")

##[Session Route] Create Session
# This route is used to create a new session based on the form data provided in the POST request.
# Note: Make sure input validation is done html side AND server side to prevent SQL injection and XSS attacks.
@app.route('/create-session', methods=['POST'])
def create_session():
    # Extract data from the form
    title = request.form.get('title')                                           # Get the title from the form data
    date = request.form.get('date')
    start_time = request.form.get('start_time')
    status = request.form.get('status')

    # Assuming there might be multiple teachers and presenters, possibly sent as comma-separated values
    teachers = request.form.get('teacherSearch').split(',') if request.form.get('teacherSearch') else []
    presenters = request.form.get('presenterSearch').split(',') if request.form.get('presenterSearch') else []

    # Input validation
    if not title or not date or not start_time or not status:                   # Check if any of the required fields are missing
        return redirect(url_for('app_routes.sessions')), 400                    # Redirect to the sessions page with a 400 Bad Request status
    
    # Convert date and time strings to datetime objects
    try:                                                                        # Try to convert the date and time strings to datetime objects
        date = datetime.strptime(date, '%Y-%m-%d').date()                           # Convert the date string to a date object
        start_time = datetime.strptime(start_time, '%H:%M').time()                  # Convert the time string to a time object
    except ValueError as e:                                                     # Handle any value errors
       return redirect(url_for('app_routes.sessions')), 400                         # Redirect to the sessions page with a 400 Bad Request status   
    
    try:                                                                                    # Try to create a new session                       
        new_session = Session(title=title, date=date, start_time=start_time, status=status)     # Create a new session object
        db.session.add(new_session)                                                             # Add the session to the database
        db.session.commit()                                                                     # Commit the changes             
    except Exception as e:                                                                  # Handle any exceptions
        db.session.rollback()                                                               # Rollback the session
        return redirect(url_for('app_routes.sessions')), 500                                # Redirect to the sessions page with a 500 Internal Server Error status
    return redirect(url_for('app_routes.sessions'))                                         # Redirect to the sessions page

##[Session Route] Search Teachers
# This route is used to search teachers based on the teacher name provided in the query parameters.
# It fetches the teachers from the database and renders the teacher list on the page for the search results.
@app.route("/search-teachers", methods=["GET"])
def search_teachers():
    teacher_name = request.args.get('teacherSearch')                                        # Get the teacher name from the query parameters
    teachers = Teacher.query.filter(Teacher.name.ilike(f'%{teacher_name}%')).all()          # Filter the teachers based on the teacher name
    return render_template("/partials/teacher_list.html", teachers=teachers)                # Render the teacher list on the page

##[Session Route] Search Presenters
# This route is used to search presenters based on the presenter name provided in the query parameters.
# It fetches the presenters from the database and renders the presenter list on the page for the search results.
@app.route("/search-presenters", methods=["GET"])
def search_presenters():
    presenter_name = request.args.get('presenterSearch')                                    # Get the presenter name from the query parameters
    presenters = Presenter.query.filter(Presenter.name.ilike(f'%{presenter_name}%')).all()  # Filter the presenters based on the presenter name
    return render_template("/partials/presenter_list.html", presenters=presenters)          # Render the presenter list on the page