import csv
from datetime import datetime
from app import db, app
from app.models import Session, Teacher, Presenter, School

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
    # Extracts the start time from a time range string.
    # Assumes time range is formatted as "HH:MM-HH:MM(am/pm)"
    if '-' in time_str:
        start_time_str = time_str.split('-')[0].strip()
        am_pm = time_str.split('-')[1].strip()[-2:]  # Extracts the AM/PM part
        start_time_str += am_pm  # Appends AM/PM to the start time
    else:
        start_time_str = time_str

    try:
        return datetime.strptime(start_time_str, '%I:%M%p').time()
    except ValueError as e:
        print(f"Error parsing time: {e}")
        return None

def import_data(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
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

            # Presenter
            presenter, created = get_or_create(
                Presenter,
                name=row['Presenter'].strip(),
                defaults={
                    'organization': row['Organization'].strip(),
                    'local': row['Presenter Location'] == 'Local'
                }
            )

            # Session
            session_date = datetime.strptime(row['Date'], '%m/%d/%Y').date() if row['Date'] else None
            session_time_str = row['Time'].strip()
            session_time = parse_start_time(session_time_str) if session_time_str else None

            if not session_date or not session_time:
                print(f"Skipping row due to invalid date or time: {row}")
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

            # Ensure that each teacher, presenter, and school is only added once to the session
            if teacher not in session.teachers:
                session.teachers.append(teacher)
            if presenter not in session.presenters:
                session.presenters.append(presenter)
            if school not in session.schools:
                session.schools.append(school)

            db.session.add(session)

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables based on the models defined
        csv_file_path = 'polaris-data.csv'  # Update this to your CSV file path
        import_data(csv_file_path)
        print('Data has been successfully imported into the database.')
