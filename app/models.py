from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import case, func, select
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from . import db

# Base Class
class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

# Association tables for many-to-many relationships
session_teachers_association = db.Table('session_teachers_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'))
)

session_schools = db.Table('session_schools',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
)

# Association table for many-to-many relationship between sessions and organizations
session_organizations_association = db.Table('session_organizations_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'), primary_key=True)
)

# Association table for many-to-many relationship between volunteers and organizations
volunteer_organizations = db.Table('volunteer_organizations',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True),
    db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'), primary_key=True)
)

# Association table for many-to-many relationship between volunteers and sessions
volunteer_sessions = db.Table('volunteer_sessions',
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True)
)

# Assocation table for many-to-many relationship between sessions and students
session_students_association = db.Table('session_students_association',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)

# Session Table
class Session(Base):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    type = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    topic = db.Column(db.String, nullable=True)
    manual_student_count = db.Column(db.Integer, nullable=True)
    skills_needed = db.Column(db.String, nullable=True)
    pathway = db.Column(db.String, nullable=True)

    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='sessions', overlaps="historical_affiliation,sessions")
    schools = db.relationship('School', secondary=session_schools, back_populates='sessions')
    organizations = db.relationship('Organization', secondary=session_organizations_association, back_populates='sessions')
    volunteers = db.relationship('Volunteer', secondary=volunteer_sessions, back_populates='sessions')
    students = db.relationship('Student', secondary=session_students_association, back_populates='sessions')

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
    
# Organization Table
class Organization(Base):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    sessions = db.relationship('Session', secondary=session_organizations_association, back_populates='organizations')
    volunteers = db.relationship('Volunteer', secondary=volunteer_organizations, back_populates='organizations', overlaps="historical_affiliation,organizations")

# Person Base Table
class PersonBase(Base):
    __abstract__ = True
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    suffix = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)
    primary_phone = db.Column(db.String(15), nullable=True)
    secondary_phone = db.Column(db.String(15), nullable=True)
    active = db.Column(db.Boolean, default=True)
    birthday = db.Column(db.Date, nullable=True)
    connector_account_id = db.Column(db.Integer, db.ForeignKey('connector_accounts.id'), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_type = db.Column(db.String(50), nullable=True)

    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @name.expression
    def name(cls):
        return cls.first_name + ' ' + cls.last_name

# Volunteer Table
class Volunteer(PersonBase):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    historical_affiliation = db.relationship('Organization', secondary=volunteer_organizations, back_populates='volunteers', overlaps="organizations")
    education_background = db.Column(db.String(100), nullable=True)
    last_mailchimp_email_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_volunteer_date = db.Column(db.DateTime, default=datetime.utcnow)
    organizations = db.relationship('Organization', secondary=volunteer_organizations, back_populates='volunteers', overlaps="historical_affiliation,volunteers")
    sessions = db.relationship('Session', secondary=volunteer_sessions, back_populates='volunteers')

    @hybrid_property
    def primary_affiliation_name(self):
        organization = next((org for org in self.organizations if org.id == self.primary_affiliation_id), None)
        return organization.name if organization else None

    @primary_affiliation_name.expression
    def primary_affiliation_name(cls):
        OrganizationAlias = aliased(Organization)
        return (
            select([OrganizationAlias.name])
            .where(OrganizationAlias.id == cls.primary_affiliation_id)
            .as_scalar()
        )

# School Table
class School(Base):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    district = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    sessions = db.relationship('Session', secondary=session_schools, back_populates='schools')
    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='historical_affiliation', overlaps="sessions,teachers")
    students = db.relationship('Student', back_populates='primary_affiliation', overlaps="sessions,students")  # Add this line


# Teacher Table
class Teacher(PersonBase):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    primary_affiliation = db.relationship('School', back_populates='teachers')
    historical_affiliation = db.relationship(
        'School',
        secondary=session_teachers_association,
        primaryjoin=(session_teachers_association.c.teacher_id == id),
        secondaryjoin=(session_teachers_association.c.school_id == School.id),
        back_populates='teachers',
        overlaps="teachers"
    )
    type = db.Column(db.String(50), nullable=False)
    sessions = db.relationship('Session', secondary=session_teachers_association, back_populates='teachers', overlaps="historical_affiliation,teachers")

    @hybrid_property
    def primary_affiliation_name(self):
        return self.primary_affiliation.name

    @primary_affiliation_name.expression
    def primary_affiliation_name(cls):
        SchoolAlias = aliased(School)
        return (
            select([SchoolAlias.name])
            .where(SchoolAlias.id == cls.primary_affiliation_id)
            .as_scalar()
        )

# Student Table
class Student(PersonBase):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    primary_affiliation = db.relationship('School', back_populates='students')
    historical_affiliation = db.relationship(
        'School',
        secondary=session_schools,
        primaryjoin=(session_schools.c.school_id == primary_affiliation_id),
        secondaryjoin=(session_schools.c.school_id == id),
        back_populates='students'
    )
    graduation_year = db.Column(db.Integer, nullable=False)
    sessions = db.relationship('Session', secondary=session_students_association, back_populates='students')  # Add this line


# Connector Account Table
class ConnectorAccount(Base):
    __tablename__ = 'connector_accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
