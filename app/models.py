from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Time, case, func, select
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased, relationship, backref
from . import db

# Association tables
session_teachers_association = db.Table('session_teachers_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'))
)

session_schools = db.Table('session_schools',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id')),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'))
)

session_students_association = db.Table('session_students_association',
    db.Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    db.Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    db.Column('school_id', Integer, ForeignKey('schools.id'), primary_key=True)  # Add this line
)

volunteer_sessions = db.Table('volunteer_sessions',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id')),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'))
)

volunteer_organizations = db.Table('volunteer_organizations',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id')),
    db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'))
)

session_organizations_association = db.Table('session_organizations_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id')),
    db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'))
)

# Base Class
class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

class Person(Base):
    __tablename__ = 'persons'
    id =db.Column(Integer, primary_key=True)
    first_name =db.Column(String(50), nullable=False)
    last_name =db.Column(String(50), nullable=False)
    middle_name =db.Column(String(50), nullable=True)
    suffix =db.Column(String(10), nullable=True)
    email =db.Column(String(100), nullable=False, unique=True)
    address =db.Column(String(255), nullable=True)
    primary_phone =db.Column(String(15), nullable=True)
    secondary_phone =db.Column(String(15), nullable=True)
    active =db.Column(Boolean, default=True)
    birthday =db.Column(Date, nullable=True)
    connector_account_id =db.Column(Integer, ForeignKey('connector_accounts.id'), nullable=True)
    gender =db.Column(String(10), nullable=True)
    contact_type =db.Column(String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': contact_type
    }

    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @name.expression
    def name(cls):
        return (cls.first_name + " " + cls.last_name)

class School(Base):
    __tablename__ = 'schools'
    id =db.Column(Integer, primary_key=True)
    name =db.Column(String(100), nullable=False, unique=True)
    district =db.Column(String(100), nullable=False)
    level =db.Column(String(50), nullable=False)
    teachers = db.relationship('Teacher', back_populates='primary_affiliation', overlaps="teachers,sessions")
    students = relationship('Student', secondary=session_students_association, back_populates='historical_affiliation', overlaps="schools,sessions")
    sessions = relationship('Session', secondary='session_schools', back_populates='schools')

class Session(Base):
    __tablename__ = 'sessions'
    id =db.Column(Integer, primary_key=True)
    name =db.Column(String(50), nullable=False, index=True)
    organization_id =db.Column(Integer, ForeignKey('organizations.id'), nullable=True)
    type =db.Column(String, nullable=False)
    status =db.Column(String, nullable=False)
    start_date =db.Column(Date, nullable=False)
    start_time =db.Column(Time, nullable=False)
    end_time =db.Column(Time, nullable=False)
    topic =db.Column(String, nullable=True)
    manual_student_count =db.Column(Integer, nullable=True)
    skills_needed =db.Column(String, nullable=True)
    pathway =db.Column(String, nullable=True)
    volunteers_needed =db.Column(Integer, nullable=False)
    location =db.Column(String, nullable=True)
    address =db.Column(String, nullable=True)
    other_info =db.Column(String, nullable=True)
    notes =db.Column(String, nullable=True)
    description =db.Column(String, nullable=True)

    teachers = relationship('Teacher', secondary='session_teachers_association', back_populates='sessions', overlaps="historical_affiliation,sessions")
    schools = relationship('School', secondary='session_schools', back_populates='sessions')
    organizations = relationship('Organization', secondary='session_organizations_association', back_populates='sessions')
    volunteers = relationship('Volunteer', secondary='volunteer_sessions', back_populates='sessions')
    students = relationship('Student', secondary='session_students_association', back_populates='sessions', overlaps="students")

    @hybrid_property
    def volunteer_count(self):
        return len(self.volunteers)

    @volunteer_count.expression
    def volunteer_count(cls):
        return (select([func.count(volunteer_sessions.c.volunteer_id)])
                .where(volunteer_sessions.c.session_id == cls.id)
                .label('volunteer_count'))

    @hybrid_property
    def student_count(self):
        if self.manual_student_count is not None:
            return self.manual_student_count
        return len(self.students)

    @student_count.expression
    def student_count(cls):
        return (
            select([func.coalesce(cls.manual_student_count, func.count(session_students_association.c.student_id))])
            .where(session_students_association.c.session_id == cls.id)
            .label('student_count')
        )

    @hybrid_property
    def participant_count(self):
        return len(self.teachers) + self.student_count + len(self.volunteers)

    @participant_count.expression
    def participant_count(cls):
        return (
            select([
                func.count(session_teachers_association.c.teacher_id) +
                func.coalesce(cls.manual_student_count, func.count(session_students_association.c.student_id)) +
                func.count(volunteer_sessions.c.volunteer_id)
            ])
            .where(session_teachers_association.c.session_id == cls.id)
            .where(session_students_association.c.session_id == cls.id)
            .where(volunteer_sessions.c.session_id == cls.id)
            .label('participant_count')
        )

    @hybrid_property
    def delivery_hours(self):
        start_dt = datetime.combine(self.start_date, self.start_time)
        end_dt = datetime.combine(self.start_date, self.end_time)
        delta = end_dt - start_dt
        return delta.total_seconds() / 3600

    @delivery_hours.expression
    def delivery_hours(cls):
        return case(
            (cls.end_time > cls.start_time, (func.strftime('%s', cls.end_time) - func.strftime('%s', cls.start_time)) / 3600),
            else_=(func.strftime('%s', cls.end_time) - func.strftime('%s', cls.start_time)) / 3600,
        ).label('delivery_hours')

class Teacher(Person):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, ForeignKey('persons.id'), primary_key=True)
    primary_affiliation_id =db.Column(Integer, ForeignKey('schools.id'), nullable=False)
    primary_affiliation = relationship('School', back_populates='teachers')
    historical_affiliation = relationship(
        'School',
        secondary='session_teachers_association',
        primaryjoin=(session_teachers_association.c.teacher_id == id),
        secondaryjoin=(session_teachers_association.c.school_id == School.id),
        back_populates='teachers',
        overlaps="teachers,sessions"
    )
    type =db.Column(String(50), nullable=False)
    sessions = relationship('Session', secondary='session_teachers_association', back_populates='teachers', overlaps="historical_affiliation,teachers")

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

class Student(Person):
    __tablename__ = 'students'
    id = db.Column(db.Integer, ForeignKey('persons.id'), primary_key=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    primary_affiliation = relationship('School', back_populates='students')
    historical_affiliation = relationship(
        'School', 
        secondary=session_students_association,
        primaryjoin="Student.id == session_students_association.c.student_id",
        secondaryjoin="School.id == session_students_association.c.school_id",
        back_populates='students',
        overlaps="schools,sessions,students"
    )
    graduation_year = db.Column(db.Integer, nullable=True)
    sessions = relationship('Session', secondary='session_students_association', back_populates='students', overlaps="historical_affiliation,students")
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Volunteer(Person):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, ForeignKey('persons.id'), primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    primary_affiliation = db.relationship('Organization', back_populates='volunteers')
    historical_affiliation = db.relationship('Organization', secondary=volunteer_organizations,
                                             back_populates='volunteers', overlaps="organizations")
    education_background = db.Column(db.String(100), nullable=True)
    last_mailchimp_email_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_volunteer_date = db.Column(db.DateTime, default=datetime.utcnow)
    organizations = db.relationship('Organization', secondary=volunteer_organizations, back_populates='volunteers')
    sessions = db.relationship('Session', secondary=volunteer_sessions, back_populates='volunteers')

    __mapper_args__ = {
        'polymorphic_identity': 'volunteer',
    }

class Organization(Base):
    __tablename__ = 'organizations'
    id =db.Column(Integer, primary_key=True)
    name =db.Column(String(100), nullable=False, unique=True)
    volunteers = relationship('Volunteer', back_populates='primary_affiliation')
    sessions = relationship('Session', secondary='session_organizations_association', back_populates='organizations')

# Connector Account Table
class ConnectorAccount(Base):
    __tablename__ = 'connector_accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
