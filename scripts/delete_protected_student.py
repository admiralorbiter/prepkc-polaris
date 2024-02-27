import sqlite3

# Path to your SQLite database
database_path = 'app/polaris.db'

# SQL command to delete specific entries
delete_command = """
DELETE FROM users
WHERE name = 'Student Protected Data Student Protected Data';
"""

# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

# Execute the delete command
try:
    cursor.execute(delete_command)
    # Commit the changes to the database
    conn.commit()
    print("Entries deleted successfully.")
except sqlite3.Error as e:
    # Rollback any changes if something goes wrong
    conn.rollback()
    print(f"An error occurred: {e}")

# Close the database connection
conn.close()