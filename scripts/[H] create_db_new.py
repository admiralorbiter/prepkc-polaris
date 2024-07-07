import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('polaris.db')
c = conn.cursor()

# Create the 'schools' table
c.execute('''
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY,
    name TEXT,
    district TEXT,
    level TEXT,
    state TEXT
)
''')

# Create the 'sessions' table
c.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    status TEXT,
    date DATE,
    start_time TIME,
    session_type TEXT,
    external_session_id INTEGER,
    title TEXT,
    topic TEXT,
    session_link TEXT
)
''')

# Create the 'volunteers' table
c.execute('''
CREATE TABLE IF NOT EXISTS volunteers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    organization TEXT,
    local BOOLEAN,
    ethnicity TEXT,
    job_title TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    session_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
)
''')

# Create the 'teachers' table
c.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    school_name TEXT
)
''')

# Create the 'session_teachers_association' table for the many-to-many relationship between sessions and teachers
c.execute('''
CREATE TABLE IF NOT EXISTS session_teachers_association (
    session_id INTEGER,
    teacher_id INTEGER,
    PRIMARY KEY (session_id, teacher_id),
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
)
''')

# Create the 'session_schools' table for the many-to-many relationship between sessions and schools
c.execute('''
CREATE TABLE IF NOT EXISTS session_schools (
    session_id INTEGER,
    school_id INTEGER,
    PRIMARY KEY (session_id, school_id),
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (school_id) REFERENCES schools(id)
)
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
