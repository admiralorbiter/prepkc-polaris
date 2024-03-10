import sqlite3
import pandas as pd

# Connect to the Polaris database
conn = sqlite3.connect('polaris.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS districts (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY,
    name TEXT,
    district_id INTEGER,
    level TEXT,
    FOREIGN KEY (district_id) REFERENCES districts(id)
)
''')

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

c.execute('''
CREATE TABLE IF NOT EXISTS presenters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    organization TEXT,
    local BOOLEAN,
    ethnicity TEXT,
    session_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    school_name TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS session_teachers (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    teacher_id INTEGER,
    status TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
)
''')

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

def insert_districts_and_schools_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        # Check if the district exists and get its ID, insert if not present
        c.execute('SELECT id FROM districts WHERE name = ?', (row['District'],))
        district_id = c.fetchone()
        if not district_id:
            c.execute('INSERT INTO districts (name) VALUES (?)', (row['District'],))
            conn.commit()
            district_id = c.lastrowid
        else:
            district_id = district_id[0]

        # Insert school with the district_id
        c.execute('''
        INSERT INTO schools (name, district_id, level) VALUES (?, ?, ?)
        ''', (row['School'], district_id, row['Level']))
    conn.commit()

# Call the function to insert schools
insert_districts_and_schools_from_csv('school-database.csv')

# Close the connection
conn.close()
