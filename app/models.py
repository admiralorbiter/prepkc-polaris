from flask_sqlalchemy import SQLAlchemy
from app import db

# Association table for the many-to-many relationship between sessions and schools
session_schools = db.Table('session_schools',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
)

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)  # Status updated by user
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)  # Renamed from start_name for clarity
    session_type = db.Column(db.String)  # User input
    external_session_id = db.Column(db.Integer)  # Renamed from session_id for clarity
    session_teachers = db.relationship('SessionTeacher', back_populates='session', lazy='dynamic')  # Renamed for clarity
    schools = db.relationship('School', secondary=session_schools, back_populates='sessions')
    title = db.Column(db.String)  # From CSV
    topic = db.Column(db.String)  # User input
    session_link = db.Column(db.String)  # User input
    presenters = db.relationship('Presenter', back_populates='session')  # Corrected to 'Presenter'

class Presenter(db.Model):  # Renamed for consistency
    __tablename__ = 'presenters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    organization = db.Column(db.String)
    local = db.Column(db.Boolean)
    ethnicity = db.Column(db.String)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    session = db.relationship('Session', back_populates='presenters')

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    school_name = db.Column(db.String)
    session_teachers = db.relationship('SessionTeacher', back_populates='teacher', lazy='dynamic')  # Renamed for clarity

class SessionTeacher(db.Model):
    __tablename__ = 'session_teachers'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    status = db.Column(db.String)  # Status updated by the user
    session = db.relationship('Session', back_populates='session_teachers')
    teacher = db.relationship('Teacher', back_populates='session_teachers')

class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    schools = db.relationship('School', back_populates='district')

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    district = db.relationship('District', back_populates='schools')
    level = db.Column(db.String)
    sessions = db.relationship('Session', secondary=session_schools, back_populates='schools')

### Tables from the original CSVs ### Tables from the original CSVs ### Tables from the original CSVs ###
class SessionRow(db.Model):
    __tablename__ = 'session_rows'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    series_or_event_title = db.Column(db.String)
    career_cluster = db.Column(db.String)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    duration = db.Column(db.Integer)
    user_auth_id = db.Column(db.Integer)
    name = db.Column(db.String)
    sign_up_role = db.Column(db.String)
    school = db.Column(db.String)
    district_or_company = db.Column(db.String)
    partner = db.Column(db.String)
    state = db.Column(db.String(2))
    registered_student_count = db.Column(db.Integer)
    attended_student_count = db.Column(db.Integer)
    registered_educator_count = db.Column(db.Integer)
    attended_educator_count = db.Column(db.Integer)
    work_based_learning = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.Integer)
    sign_up_role = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    login_email = db.Column(db.String, nullable=False, unique=True)
    notification_email = db.Column(db.String, unique=True)
    school = db.Column(db.String)
    district_or_company = db.Column(db.String)
    job_title = db.Column(db.String)
    grade_cluster = db.Column(db.String)
    skills = db.Column(db.String)
    join_date = db.Column(db.Date)
    last_login_date = db.Column(db.Date)
    login_count = db.Column(db.Integer)
    count_of_days_logged_in_last_30_days = db.Column(db.Integer)
    city = db.Column(db.String)
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String)
    active_subscription_type = db.Column(db.String)
    active_subscription_name = db.Column(db.String)
    last_session_date = db.Column(db.Date)
    affiliations = db.Column(db.String)