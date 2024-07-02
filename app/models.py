from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    delivery_hours = db.Column(db.Numeric, nullable=False)
    topic = db.Column(db.String, nullable=True)
    participant_count = db.Column(db.Integer, nullable=False)
    student_count = db.Column(db.Integer, nullable=False)
    volunteer_count = db.Column(db.Integer, nullable=False)
    skills_needed = db.Column(db.String, nullable=True)
    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='sessions', overlaps="historical_affiliation,sessions")
    schools = db.relationship('School', secondary=session_schools, back_populates='sessions')
    organizations = db.relationship('Organization', secondary=session_organizations_association, back_populates='sessions')

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
    address = db.Column(db.String(255), nullable=False)
    primary_phone = db.Column(db.String(15), nullable=False)
    secondary_phone = db.Column(db.String(15), nullable=True)
    active = db.Column(db.Boolean, default=True)
    birthday = db.Column(db.Date, nullable=False)
    connector_account_id = db.Column(db.Integer, db.ForeignKey('connector_accounts.id'), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_type = db.Column(db.String(50), nullable=True)

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

# School Table
class School(Base):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    district = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    sessions = db.relationship('Session', secondary=session_schools, back_populates='schools')
    teachers = db.relationship('Teacher', secondary=session_teachers_association, back_populates='historical_affiliation', overlaps="sessions,teachers")

# Teacher Table
class Teacher(PersonBase):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    primary_affiliation_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
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

# Connector Account Table
class ConnectorAccount(Base):
    __tablename__ = 'connector_accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
