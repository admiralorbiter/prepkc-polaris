from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

## Base Class
# This class is used to define the common columns that are used in all the tables.
class Base(db.Model):
    __abstract__ = True                                                                         # Indicates that this class should not be created as a table
    created_at = db.Column(db.DateTime, default=datetime.utcnow)                                # This column will be set to the current time when a row is created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)      # This column will be updated whenever the row is updated
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)                              # Soft delete column

# The `session_teachers_association` table is an association table that establishes a many-to-many relationship between sessions and teachers.
# It has two columns: `session_id` and `teacher_id`. Both are integers and serve as primary keys.
session_teachers_association = db.Table('session_teachers_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
)

# Similarly, the `session_schools` table is an association table that establishes a many-to-many relationship between sessions and schools.
# It also has two columns: `session_id` and `school_id`. Both are integers and serve as primary keys.
session_schools = db.Table('session_schools',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
)

## Session Table
# This table stores information about the sessions that are conducted.
class Session(db.Model):
    __tablename__ = 'sessions'                                                                  # Table name
    id = db.Column(db.Integer, primary_key=True)                                                # Primary key created on when a session is created
    status = db.Column(db.String, index=True)                                                   # Status of the session 
    date = db.Column(db.Date, index=True)                                                       # Date of the session
    start_time = db.Column(db.Time, index=True)                                                 # Start time of the session
    session_type = db.Column(db.String)                                                         # Type of the session
    external_session_id = db.Column(db.Integer)                                                 # External session id based on the connector        
    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='sessions')
    schools = db.relationship('School', secondary=session_schools, back_populates='sessions')
    title = db.Column(db.String)                                                                # Title of the session                          
    topic = db.Column(db.String)                                                                # Topic of the session
    session_link = db.Column(db.String)                                                         # Link to the session
    presenters = db.relationship('Presenter', back_populates='session')                         # Relationship with the Presenter table

    @property
    def school_teacher_mapping(self):
        mapping = defaultdict(list)
        for teacher in self.teachers:  # Assuming 'teachers' is a relationship field in the model
            mapping[teacher.school_name].append(teacher.name)
        return mapping

## Presenter Table
# This table stores information about the presenters who conduct the sessions.
class Presenter(db.Model):
    __tablename__ = 'presenters'                                                                # Table name                
    id = db.Column(db.Integer, primary_key=True)                                                # Primary key created on when a presenter is created
    name = db.Column(db.String)                                                                 # Name of the presenter
    email = db.Column(db.String, index=True)                                                    # Email of the presenter
    phone = db.Column(db.String)                                                                # Phone number of the presenter
    organization = db.Column(db.String)                                                         # Organization of the presenter                           
    local = db.Column(db.Boolean)                                                               # Local or not boolean
    ethnicity = db.Column(db.String)                                                            # ethnicity of the presenter
    job_title = db.Column(db.String)                                                            # Job title of the presenter
    city = db.Column(db.String)
    state = db.Column(db.String(2))                                                             # State of the presenter                                :up to 2 characters
    postal_code = db.Column(db.String)                                                          # Postal code of the presenter
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), index=True)                # Foreign key to the Session table
    session = db.relationship('Session', back_populates='presenters')                           # Relationship with the Session table

## Teacher Table
# This table stores information about the teachers who are part of the sessions.
class Teacher(db.Model):
    __tablename__ = 'teachers'                                                                  # Table name
    id = db.Column(db.Integer, primary_key=True)                                                # Primary key created on when a teacher is created
    name = db.Column(db.String)                                                                 # Name of the teacher
    school_name = db.Column(db.String)                                                          # School name of the teacher
    sessions = db.relationship('Session', secondary=session_teachers_association, back_populates='teachers')

class School(db.Model):
    __tablename__ = 'schools'                                                                   # Table name
    id = db.Column(db.Integer, primary_key=True)                                                # Primary key created on when a school is created
    name = db.Column(db.String)                                                                 # Name of the school             
    district = db.Column(db.String)                                                             # District of the school             
    level = db.Column(db.String)                                                                # Level of the school
    state = db.Column(db.String(2))                                                             # State of the school                                :up to 2 characters
    sessions = db.relationship('Session', secondary=session_schools, back_populates='schools')  # Relationship with the Session table