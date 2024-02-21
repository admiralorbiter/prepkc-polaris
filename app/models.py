from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'
    
    session_id = db.Column(db.Integer, primary_key=True)
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
    
    user_auth_id = db.Column(db.Integer, primary_key=True)
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
