from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

# New association table for the many-to-many relationship between sessions and teachers
session_teachers_association = db.Table('session_teachers_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
)

# Association table for the many-to-many relationship between sessions and schools
session_schools = db.Table('session_schools',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
)

class Base(db.Model):
    __abstract__ = True  # Indicates that this class should not be created as a table

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)  # Soft delete column

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, index=True)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time, index=True) 
    session_type = db.Column(db.String) 
    external_session_id = db.Column(db.Integer)  
    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='sessions')
    schools = db.relationship('School', secondary=session_schools, back_populates='sessions')
    title = db.Column(db.String) 
    topic = db.Column(db.String)  
    session_link = db.Column(db.String) 
    presenters = db.relationship('Presenter', back_populates='session')

class Presenter(db.Model):
    __tablename__ = 'presenters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, index=True)
    phone = db.Column(db.String)
    organization = db.Column(db.String)
    local = db.Column(db.Boolean)
    ethnicity = db.Column(db.String)
    job_title = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), index=True)
    session = db.relationship('Session', back_populates='presenters')

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    school_name = db.Column(db.String)
    sessions = db.relationship('Session', secondary=session_teachers_association, back_populates='teachers')


class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    district = db.Column(db.String)
    level = db.Column(db.String)
    state = db.Column(db.String(2))
    sessions = db.relationship('Session', secondary=session_schools, back_populates='schools')

### Tables from the original CSVs ### Tables from the original CSVs ### Tables from the original CSVs ###
class SessionRow(db.Model):
    __tablename__ = 'session_rows'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    series_or_event_title = db.Column(db.String)
    career_cluster = db.Column(db.String) #Missing
    date = db.Column(db.Date)
    status = db.Column(db.String)
    duration = db.Column(db.Integer)
    user_auth_id = db.Column(db.Integer)
    name = db.Column(db.String)
    sign_up_role = db.Column(db.String)
    school = db.Column(db.String)
    district_or_company = db.Column(db.String)
    partner = db.Column(db.String)
    state = db.Column(db.String(2)) #missing add to sschool
    registered_student_count = db.Column(db.Integer) #Missing
    attended_student_count = db.Column(db.Integer) #Missing
    registered_educator_count = db.Column(db.Integer) #Missing
    attended_educator_count = db.Column(db.Integer) #Missing
    work_based_learning = db.Column(db.String) #Missing

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
    skills = db.Column(db.String) #missing
    join_date = db.Column(db.Date) #missing
    last_login_date = db.Column(db.Date) #missing
    login_count = db.Column(db.Integer) #missing
    count_of_days_logged_in_last_30_days = db.Column(db.Integer) #missing
    city = db.Column(db.String)
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String)
    active_subscription_type = db.Column(db.String) #missing
    active_subscription_name = db.Column(db.String) #missing
    last_session_date = db.Column(db.Date)
    affiliations = db.Column(db.String) #missing

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    affiliation = db.Column(db.String(255), nullable=True)
    job_category = db.Column(db.String(255), nullable=True)
    skills_text = db.Column(db.Text, nullable=True)  # For the textual description of skills
    skills = db.Column(db.Text, nullable=True)  # You might want to use a more structured way to store multiple skills, like a relationship to another table

    def __repr__(self):
        return f'<Volunteer {self.name}>'