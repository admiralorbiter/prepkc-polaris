import csv
from datetime import datetime
from app import db, app
from app.models.models import Session, Teacher, volunteer, School
import re

def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True

def parse_start_time(time_str):
    # Normalize the time string by removing extra spaces and correcting common typos
    time_str = time_str.replace(';', ':').replace(' ', '').lower()

    # Define a pattern to match time formats, including those without minutes
    time_pattern = r'(\d{1,2})(?::(\d{2}))?(am|pm)'

    # Try to find a match for the time pattern
    match = re.search(time_pattern, time_str)
    if match:
        hour, minute, am_pm = match.groups()
        hour = int(hour)
        minute = int(minute) if minute else 0  # Default to 0 if no minutes are specified

        # Convert to 24-hour format if needed
        if am_pm == 'pm' and hour < 12:
            hour += 12
        elif am_pm == 'am' and hour == 12:
            hour = 0

        # Construct the time object
        try:
            return datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
        except ValueError as e:
            print(f"Error parsing time: {e}")

    print(f"Unable to parse time: {time_str}")
    return None

def import_data(csv_file_path):
    session_map = {}  # Maps session titles to session instances

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            session_title = row['Session Title'].strip()
            session_date = datetime.strptime(row['Date'], '%m/%d/%Y').date() if row['Date'] else None
            session_status = row['Status'].strip()
            # School
            school, created = get_or_create(
                School,
                name=row['School Name'].strip(),
                defaults={
                    'level': row['School Level'].strip(),
                    'district': row['District'].strip()
                }
            )

            # Teacher
            teacher, created = get_or_create(
                Teacher,
                name=row['Teacher Name'].strip(),
                defaults={'school_name': school.name}
            )

            # volunteer
            volunteer, created = get_or_create(
                volunteer,
                name=row['volunteer'].strip(),
                defaults={
                    'organization': row['Organization'].strip(),
                    'local': row['volunteer Location'] == 'Local'
                }
            )

            # Check if this session title has already been encountered
            if session_title in session_map:
                session = session_map[session_title]
                if session_status.lower() == 'simulcast':
                    # For simulcast, just associate new teachers and schools without creating a new session
                    if teacher not in session.teachers:
                        session.teachers.append(teacher)
                    if school not in session.schools:
                        session.schools.append(school)
                    continue  # Move to the next row without creating a new session or changing existing session details
            else:
                # This is a new session or the first entry of a session
                session_time_str = row['Time'].strip()
                session_time = parse_start_time(session_time_str) if session_time_str else None

                if not session_time:
                    print(f"Skipping session due to missing start time: {session_title}")
                    continue


                session, created = get_or_create(
                    Session,
                    title=row['Session Title'].strip(),
                    defaults={
                        'status': row['Status'].strip(),
                        'date': session_date,
                        'start_time': session_time,
                        'session_type': row['Session Type'].strip(),
                        'topic': row['Topic/Theme'].strip(),
                        'session_link': row['Session Link'].strip()
                    }
                )

                # Ensure that each teacher, volunteer, and school is only added once to the session
                if teacher not in session.teachers:
                    session.teachers.append(teacher)
                if volunteer not in session.volunteers:
                    session.volunteers.append(volunteer)
                if school not in session.schools:
                    session.schools.append(school)
                session_map[session_title] = session
            db.session.add(session)

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables based on the models defined
        csv_file_path = 'polaris-data.csv'  # Update this to your CSV file path
        import_data(csv_file_path)
        print('Data has been successfully imported into the database.')
