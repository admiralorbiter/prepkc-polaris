from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
from app import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polaris.db'
db = SQLAlchemy(app)

# Assuming your models.py defines models named 'Session' and 'User'
Session = models.Session
User = models.User

def insert_sessions():
    # Load session data from CSV
    session_df = pd.read_csv('session.csv')
    session_df['Registered Student Count'] = session_df['Registered Student Count'].fillna(0).astype(int)
    session_df['Attended Student Count'] = session_df['Attended Student Count'].fillna(0).astype(int)
    session_df['Registered Educator Count'] = session_df['Registered Educator Count'].fillna(0).astype(int)
    session_df['Attended Educator Count'] = session_df['Attended Educator Count'].fillna(0).astype(int)
    for _, row in session_df.iterrows():
        if not isinstance(row['Date'], str):
            print(f"Skipping row with invalid date: {row}")
            continue  # Skip this row
        session = Session(
            session_id=row['Session ID'],
            title=row['Title'],
            series_or_event_title=row['Series or Event Title'],
            career_cluster=row['Career Cluster'],
            date=datetime.strptime(row['Date'], '%m/%d/%Y'),
            status=row['Status'],
            duration=int(row['Duration']),
            user_auth_id=int(row['User Auth Id']),
            name=row['Name'],
            sign_up_role=row['SignUp Role'],
            school=row['School'],
            district_or_company=row['District or Company'],
            partner=row['Partner'],
            state=row['State'],
            registered_student_count=row['Registered Student Count'],  # This field is now an integer
            attended_student_count=row['Attended Student Count'],  # This field is now an integer
            registered_educator_count=row['Registered Educator Count'],  # This field is now an integer
            attended_educator_count=row['Attended Educator Count'],  # This field is now an integer
            work_based_learning=row['Work Based Learning']
        )
        db.session.add(session)
    db.session.commit()

def insert_users():
    # Load user data from CSV
    user_df = pd.read_csv('user.csv')
    for _, row in user_df.iterrows():
        user = User(
            user_auth_id=row['UserAuthId'],
            sign_up_role=row['SignUpRole'],
            name=row['Name'],
            login_email=row['LoginEmail'],
            notification_email=row['NotificationEmail'],
            school=row['School'],
            district_or_company=row['District or Company'],
            job_title=row['JobTitle'],
            grade_cluster=row['GradeCluster'],
            skills=row['Skills'],
            join_date=datetime.strptime(row['JoinDate'], '%m/%d/%Y') if pd.notnull(row['JoinDate']) else None,
            last_login_date=datetime.strptime(row['LastLoginDate'], '%m/%d/%Y') if pd.notnull(row['LastLoginDate']) else None,
            login_count=int(row['LoginCount']),
            count_of_days_logged_in_last_30_days=int(row['CountOfDaysLoggedInLast30Days']),
            city=row['City'],
            state=row['State'],
            postal_code=row['PostalCode'],
            active_subscription_type=row['ActiveSubscriptionType'],
            active_subscription_name=row['ActiveSubscriptionName'],
            last_session_date=datetime.strptime(row['LastSessionDate'], '%m/%d/%Y') if pd.notnull(row['LastSessionDate']) else None,
            affiliations=row['Affiliations']
        )
        db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will now execute within the application context
        insert_sessions()
        insert_users()