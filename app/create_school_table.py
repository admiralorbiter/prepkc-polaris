import sqlite3
import pandas as pd

# Data for the schools table
data = {
    "school": [
        "CENTER HIGH SCHOOL", "CENTER ALTERNATIVE", "GRANDVIEW MIDDLE", "GRANDVIEW SR. HIGH",
        "COMPASS ELEMENTARY", "DOBBS ELEM.", "EARLY CHILDHOOD CTR.", "ERVIN ELEMENTARY",
        "INGELS ELEM.", "MILLENNIUM AT SANTA FE", "RUSKIN HIGH SCHOOL", "SMITH-HALE MIDDLE",
        "TRUMAN ELEM.", "WARFORD ELEM.", "EAST HIGH SCHOOL", "LINCOLN COLLEGE PREP.",
        "MANUAL CAREER & TECH. CTR.", "ARGENTINE MIDDLE", "ARROWHEAD MIDDLE", "BANNEKER ELEM",
        "BERTRAM CARUTHERS ELEM", "CARL B. BRUCE MIDDLE SCHOOL", "CENTRAL MIDDLE", "CLAUDE A HUYCK ELEM",
        "D D EISENHOWER MIDDLE", "EMERSON ELEM", "EUGENE WARE ELEM", "F L SCHLAGLE HIGH",
        "FRANCES WILLARD ELEM", "FRANK RUSHTON ELEM", "GLORIA WILLIS MIDDLE SCHOOL", "GRANT ELEM",
        "HAZEL GROVE ELEM", "J C HARMON HIGH", "JOHN F KENNEDY ELEM", "JOHN FISKE ELEM",
        "LINDBERGH ELEM", "LOWELL BRUNE ELEMENTARY SCHOOL", "M E PEARSON ELEM", "MARK TWAIN ELEM",
        "MCKINLEY ELEMENTARY SCHOOL", "NEW CHELSEA ELEMENTARY", "NEW STANLEY ELEM", "QUINDARO ELEM",
        "ROSEDALE MIDDLE", "SILVER CITY ELEM", "STONY POINT NORTH", "SUMNER ACADEMY OF ARTS & SCIENCE",
        "THOMAS A EDISON ELEM", "WASHINGTON HIGH", "WEST PARK ELEMENTARY SCHOOL", "WHITTIER ELEM",
        "WYANDOTTE HIGH"
    ],
    "district": [
        "CENTER 58 SCHOOL DISTRICT", "CENTER SCHOOL DISTRICT", "GRANDVIEW C-4", "GRANDVIEW C-4",
        "HICKMAN MILLS C-1", "HICKMAN MILLS C-1", "HICKMAN MILLS C-1", "HICKMAN MILLS C-1",
        "HICKMAN MILLS C-1", "HICKMAN MILLS C-1", "HICKMAN MILLS C-1", "HICKMAN MILLS C-1",
        "HICKMAN MILLS C-1", "HICKMAN MILLS C-1", "KANSAS CITY PUBLIC SCHOOL DISTRICT", "KANSAS CITY PUBLIC SCHOOL DISTRICT",
        "KANSAS CITY PUBLIC SCHOOL DISTRICT", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500", "KANSAS CITY USD 500",
        "KANSAS CITY USD 500"
    ],
    "level": [
        "High", "High", "Middle", "High",
        "Elem", "Elem", "Elem", "Elem",
        "Elem", "Elem", "High", "Middle",
        "Elem", "Elem", "High", "High",
        "High", "Middle", "Middle", "Elem",
        "Elem", "Middle", "Middle", "Elem",
        "Middle", "Elem", "Elem", "High",
        "Elem", "Elem", "Middle", "Elem",
        "Elem", "High", "Elem", "Elem",
        "Elem", "Elem", "Elem", "Elem",
        "Elem", "Elem", "Elem", "Elem",
        "Middle", "Elem", "Elem", "High",
        "Elem", "High", "Elem", "Elem",
        "High"
    ]
}

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Connect to the SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('polaris.db')

# Create the 'schools' table if it doesn't exist
df.to_sql('schools', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Schools table created and populated successfully.")
