import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models import Person, Volunteer, Base  # Make sure your models file is correctly imported

# Database setup
engine = create_engine('sqlite:///volunteers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def log_skipped_row(row, error_message):
    with open('skipped_rows.csv', 'a', newline='') as file:
        fieldnames = list(row.keys()) + ['error']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({**row, 'error': error_message})

def import_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                person = session.query(Person).filter_by(email=row['email']).first()
                if not person:
                    person = Person(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        address=row['address'],
                        primary_phone=row['primary_phone'],
                        secondary_phone=row['secondary_phone'],
                        active=row['active'] == '1',
                        birthday=datetime.strptime(row['birthday'], '%Y-%m-%d') if row['birthday'] else None,
                        connector_account_id=row['connector_account_id'],
                        gender=row['gender'],
                        contact_type=row['contact_type'],
                        do_not_call=row['do_not_call'] == '1',
                        h_salesforce_id=row['h_salesforce_id'],
                        h_salesforce_account_id=row['h_salesforce_account_id'],
                        secondary_email=row['secondary_email'],
                        home_email=row['home_email'],
                        work_email=row['work_email'],
                        prefered_email=row['prefered_email'],
                        country_code=row['country_code'],
                        city=row['city'],
                        state=row['state'],
                        postal_code=row['postal_code'],
                        preferred_phone=row['preferred_phone'],
                        h_owner_id=row['h_owner_id'],
                        opt_out_email=row['opt_out_email'] == '1',
                        opt_out_phone=row['opt_out_phone'] == '1',
                        h_created_date=datetime.strptime(row['h_created_date'], '%Y-%m-%d %H:%M:%S') if row['h_created_date'] else None,
                        h_salesforce_primary_aff=row['h_salesforce_primary_aff'],
                        h_org_name=row['h_org_name'],
                        age_group=row['age_group'],
                        do_not_contact=row['do_not_contact'] == '1',
                        h_connector_join_date=datetime.strptime(row['h_connector_join_date'], '%Y-%m-%d %H:%M:%S') if row['h_connector_join_date'] else None,
                        h_connector_last_login_date=datetime.strptime(row['h_connector_last_login_date'], '%Y-%m-%d %H:%M:%S') if row['h_connector_last_login_date'] else None,
                        h_connecotr_join_date=datetime.strptime(row['h_connecotr_join_date'], '%Y-%m-%d %H:%M:%S') if row['h_connecotr_join_date'] else None,
                        h_connector_id=row['h_connector_id'],
                        h_first_volunteer_date=datetime.strptime(row['h_first_volunteer_date'], '%Y-%m-%d %H:%M:%S') if row['h_first_volunteer_date'] else None,
                        h_num_of_attended_sessions=row['h_num_of_attended_sessions'],
                        h_num_of_noshow_sessions=row['h_num_of_noshow_sessions'],
                        h_org_name_reported=row['h_org_name_reported'],
                        person_of_color=row['person_of_color'] == '1',
                        racial_ethnic_background=row['racial_ethnic_background'],
                        status=row['status'],
                        h_last_email_message=row['h_last_email_message'],
                        h_connector_last_update=datetime.strptime(row['h_connector_last_update'], '%Y-%m-%d %H:%M:%S') if row['h_connector_last_update'] else None,
                        h_connector_signup_role=row['h_connector_signup_role'],
                        h_last_completed_task=row['h_last_completed_task'],
                        connector_active_subscription=row['connector_active_subscription'],
                        created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S') if row['created_at'] else None,
                        updated_at=datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S') if row['updated_at'] else None,
                        deleted_at=datetime.strptime(row['deleted_at'], '%Y-%m-%d %H:%M:%S') if row['deleted_at'] else None
                    )
                    session.add(person)
                    session.flush()  # Ensure the person is added to get the ID

                volunteer = Volunteer(
                    id=person.id,
                    title=row['title'],
                    primary_affiliation_id=row['primary_affiliation_id'],
                    education_background=row['education_background'],
                    last_mailchimp_email_date=datetime.strptime(row['last_mailchimp_email_date'], '%Y-%m-%d %H:%M:%S') if row['last_mailchimp_email_date'] else None,
                    last_volunteer_date=datetime.strptime(row['last_volunteer_date'], '%Y-%m-%d %H:%M:%S') if row['last_volunteer_date'] else None,
                    h_interests=row['h_interests'],
                    h_skills_text=row['h_skills_text'],
                    h_skills=row['h_skills']
                )
                session.add(volunteer)

            except Exception as e:
                log_skipped_row(row, str(e))
                continue
    session.commit()
    print("Successfully committed the session.")

if __name__ == "__main__":
    import_data('Volunteer.csv')
