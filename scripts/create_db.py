
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('polaris.db')
c = conn.cursor()

# Create tables
# Assuming simplified structures based on the Flask models and provided CSV headers
c.execute('''CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    title TEXT,
    series_or_event_title TEXT,
    career_cluster TEXT,
    date TEXT,
    status TEXT,
    duration INTEGER,
    user_auth_id INTEGER,
    name TEXT,
    sign_up_role TEXT,
    school TEXT,
    district_or_company TEXT,
    partner TEXT,
    state TEXT,
    registered_student_count INTEGER,
    attended_student_count INTEGER,
    registered_educator_count INTEGER,
    attended_educator_count INTEGER,
    work_based_learning TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      
    user_auth_id INTEGER,
    sign_up_role TEXT,
    name TEXT,
    login_email TEXT,
    notification_email TEXT,
    school TEXT,
    district_or_company TEXT,
    job_title TEXT,
    grade_cluster TEXT,
    skills TEXT,
    join_date TEXT,
    last_login_date TEXT,
    login_count INTEGER,
    count_of_days_logged_in_last_30_days INTEGER,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    active_subscription_type TEXT,
    active_subscription_name TEXT,
    last_session_date TEXT,
    affiliations TEXT
)''')

# Commit the changes
conn.commit()

def insert_sessions():
    session_df = pd.read_csv('fake_session.csv')
    with open('skipped_sessions_log.txt', 'w') as log_file:  # Open a log file to write skipped rows
        for _, row in session_df.iterrows():
            try:
                c.execute('''INSERT INTO sessions (session_id, title, series_or_event_title, career_cluster, date, status, duration, user_auth_id, name, sign_up_role, school, district_or_company, partner, state, registered_student_count, attended_student_count, registered_educator_count, attended_educator_count, work_based_learning) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    row['Session ID'],
                    row['Title'],
                    row['Series or Event Title'],
                    row['Career Cluster'],
                    # datetime.strptime(row['Date'], '%m/%d/%Y').strftime('%Y-%m-%d') if pd.notnull(row['Date']) else None,
                    datetime.strptime(row['Date'], '%Y-%m-%d').strftime('%Y-%m-%d') if pd.notnull(row['Date']) else None,
                    row['Status'],
                    row['Duration'],
                    row['User Auth Id'],
                    row['Name'],
                    row['SignUp Role'],
                    row['School'],
                    row['District or Company'],
                    row['Partner'],
                    row['State'],
                    row['Registered Student Count'] if row['Registered Student Count'] != 'n/a' else None,
                    row['Attended Student Count'] if row['Attended Student Count'] != 'n/a' else None,
                    row['Registered Educator Count'] if row['Registered Educator Count'] != 'n/a' else None,
                    row['Attended Educator Count'] if row['Attended Educator Count'] != 'n/a' else None,
                    row['Work Based Learning']
                ))
            except Exception as e:
                log_file.write(f'Error: {e}\nRow: {row}\n\n')
    conn.commit()

def insert_users():
    user_df = pd.read_csv('fake_user.csv')
    with open('skipped_users_log.txt', 'w') as log_file:
        for _, row in user_df.iterrows():
            try:
                c.execute('''INSERT INTO users (user_auth_id, sign_up_role, name, login_email, notification_email, school, district_or_company, job_title, grade_cluster, skills, join_date, last_login_date, login_count, count_of_days_logged_in_last_30_days, city, state, postal_code, active_subscription_type, active_subscription_name, last_session_date, affiliations) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    row['UserAuthId'],
                    row['SignUpRole'],
                    row['Name'],
                    row['LoginEmail'],
                    row['NotificationEmail'],
                    row['School'],
                    row['District or Company'],
                    row['JobTitle'],
                    row['GradeCluster'],
                    row['Skills'],
                    datetime.strptime(row['JoinDate'], '%m/%d/%Y').strftime('%Y-%m-%d') if pd.notnull(row['JoinDate']) else None,
                    datetime.strptime(row['LastLoginDate'], '%m/%d/%Y').strftime('%Y-%m-%d') if pd.notnull(row['LastLoginDate']) else None,
                    row['LoginCount'],
                    row['CountOfDaysLoggedInLast30Days'],
                    row['City'],
                    row['State'],
                    row['PostalCode'],
                    row['ActiveSubscriptionType'],
                    row['ActiveSubscriptionName'],
                    datetime.strptime(row['LastSessionDate'], '%m/%d/%Y').strftime('%Y-%m-%d') if pd.notnull(row['LastSessionDate']) else None,
                    row['Affiliations']
                ))
            except Exception as e:
                log_file.write(f'Error: {e}\nRow: {row}\n\n')
    conn.commit()

if __name__ == '__main__':
    insert_sessions()
    insert_users()

    # Close the connection to the database
    conn.close()
