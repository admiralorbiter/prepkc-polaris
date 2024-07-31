import csv
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import db
from app.models.models import Volunteer

# Initialize the Flask app and database connection
persistent_path = os.getenv("PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__)))
app = Flask(__name__)
db_path = os.path.join(persistent_path, "polaris.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Define the mapping rules for all columns
FIELD_MAPPING = {
    'Id': 'h_salesforce_id',
    'AccountId': 'primary_affiliation_id',
    'npe01__AlternateEmail__c': 'secondary_email',
    'npe01__HomeEmail__c': 'home_email',
    'npe01__WorkEmail__c': 'work_email',
    'npe01__Preferred_Email__c': 'prefered_email',
    'OtherCountryCode': 'country_code',
    'MailingCity': 'city',
    'MailingState': 'state',
    'MailingPostalCode': 'postal_code',
    'Phone': 'primary_phone',
    'OwnerId': 'h_owner_id',
    'HasOptedOutOfEmail': 'opt_out_email',
    'DoNotCall': 'do_not_call',
    'CreatedDate': 'h_created_date',
    'npsp__Primary_Affiliation__c': 'h_salesforce_primary_aff',
    'organization_name': 'h_org_name',
    'Age_Group__c': 'age_group',
    'npsp__Do_Not_Contact__c': 'do_not_contact',
    'Connector_Joining_Date__c': 'h_connector_join_date',
    'Connector_Last_Login_Date_Time__c': 'h_connector_last_login_datetime',
    'Connector_User_ID__c': 'h_connector_id',
    'First_Volunteer_Date__c': 'h_first_volunteer_date',
    'Number_of_Attended_Volunteer_Sessions__c': 'h_num_of_attended_sessions',
    'Number_of_No_Show_Volunteer_Sessions__c': 'h_num_of_no_show_sessions',
    'Organization_self_reported__c': 'h_org_name_reported',
    'Person_of_Color__c': 'person_of_color',
    'Racial_Ethnic_Background__c': 'racial_background',
    'Volunteer_Interests__c': 'h_interests',
    'Volunteer_Skills_Text__c': 'h_skills_text',
    'Volunteer_Skills__c': 'h_skills',
    'Volunteer_Status__c': 'status',
    'Last_Email_Message__c': 'h_last_email_message',
    'Connector_Last_Update_Date__c': 'h_connector_last_update',
    'Connector_SignUp_Role__c': 'h_connector_signup_role',
    'Last_Completed_Task__c': 'h_last_completed_task',
    'Salutation': 'suffix',
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'Email': 'email',
    'npe01__PreferredPhone__c': 'prefered_phone',
    'Title': 'title',
    'Connector_Active_Subscription__c': 'connector_active_subscription',
    'Gender__c': 'gender',
    'Highest_Level_of_Educational__c': 'education_background',
    'Last_Mailchimp_Email_Date__c': 'last_mailchimp_email_date',
    'Last_Volunteer_Date__c': 'last_volunteer_date'
}

# List of fields that should be converted to boolean
BOOLEAN_FIELDS = [
    'do_not_call',
    'opt_out_email',
    'do_not_contact',
    'person_of_color',
    'connector_active_subscription'
]

# List of fields that should be converted to datetime
DATETIME_FIELDS = [
    'h_created_date', 'h_connector_join_date', 'h_connector_last_login_datetime',
    'h_first_volunteer_date', 'last_mailchimp_email_date', 'last_volunteer_date',
    'h_last_email_message', 'h_connector_last_update', 'h_last_completed_task'
]

def convert_to_boolean(value):
    if value in ['1', 'true', 'True', 'yes', 'Yes', 'Y']:
        return True
    if value in ['0', 'false', 'False', 'no', 'No', 'N']:
        return False
    return None

def convert_to_datetime(value):
    if value:
        try:
            # Try to parse various date formats
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                try:
                    return datetime.strptime(value, '%m/%d/%Y %I:%M %p')
                except ValueError:
                    try:
                        return datetime.strptime(value, '%m/%d/%Y')
                    except ValueError:
                        return None
    return None

def import_columns(file_path, field_mapping):
    with app.app_context():
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            skipped_rows = []

            for row in reader:
                try:
                    volunteer = Volunteer.query.filter_by(h_salesforce_id=row['Id']).first()
                    if not volunteer:
                        volunteer = Volunteer(h_salesforce_id=row['Id'])
                        db.session.add(volunteer)
                    
                    for csv_column, model_field in field_mapping.items():
                        if csv_column in row:
                            value = row[csv_column]
                            if model_field in BOOLEAN_FIELDS:
                                value = convert_to_boolean(value)
                            if model_field in DATETIME_FIELDS:
                                value = convert_to_datetime(value)
                            setattr(volunteer, model_field, value)
                    
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    skipped_rows.append((row, str(e)))

        # Log skipped rows
        with open('skipped_rows.log', 'w') as log_file:
            for skipped_row, error in skipped_rows:
                log_file.write(f"Error: {error}\nRow: {skipped_row}\n\n")

        # Verification: Print out the imported data
        imported_volunteers = Volunteer.query.all()
        print(f"Imported {len(imported_volunteers)} volunteers:")
        for v in imported_volunteers:
            print(f"Volunteer ID: {v.h_salesforce_id}, Email: {v.email}, FirstName: {v.first_name}, LastName: {v.last_name}, Phone: {v.primary_phone}, City: {v.city}, State: {v.state}, PostalCode: {v.postal_code}, Title: {v.title}, Gender: {v.gender}, HomeEmail: {v.home_email}, WorkEmail: {v.work_email}, PreferredEmail: {v.prefered_email}, OwnerID: {v.h_owner_id}")

if __name__ == "__main__":
    import_columns('Volunteer.csv', FIELD_MAPPING)
