import sqlite3

# Connect to the database file, or create it if it doesn't exist
conn = sqlite3.connect('movies.db')

# Define a cursor to interact with the database
cursor = conn.cursor()

# Define the CREATE TABLE statement
create_table_sql = """
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    liked INTEGER,
    in_library INTEGER,
    studio TEXT,
    year TEXT,
    user_rating REAL,
    rating REAL,
    summary TEXT,
    content_rating TEXT,
    genre_tags TEXT,
    duration INTEGER,
    playlist_tags TEXT
);
"""

#Define other CREATE TABLE's as needed

# Execute the statement to create the table
cursor.execute(create_table_sql)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Database setup is complete.")
