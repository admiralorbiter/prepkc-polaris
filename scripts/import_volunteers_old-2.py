import pandas as pd
from datetime import datetime
from app.models import db, Volunteer, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the database and table are created
engine = create_engine('sqlite:///polaris.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv('Volunteer.csv')

# Print columns to verify
print("CSV Columns:", df.columns)

def convert_to_int(value):
    try:
        return int(value) if not pd.isna(value) else None
    except (ValueError, TypeError):
        return None

def convert_to_bool(value):
    try:
        return bool(int(value)) if not pd.isna(value) else None
    except (ValueError, TypeError):
        return None

def convert_to_date(value):
    try:
        if pd.notna(value) and value != '':
            date_value = pd.to_datetime(value, errors='coerce')
            if pd.notna(date_value):
                return date_value.to_pydatetime()
        return None
    except (ValueError, TypeError):
        return None

for index, row in df.iterrows():
    try:
        h_first_volunteer_date = convert_to_date(row.get('First_Volunteer_Date__c'))
        h_created_date = convert_to_date(row.get('CreatedDate'))
        h_connector_join_date = convert_to_date(row.get('Connector_Joining_Date__c'))
        h_connector_last_login_date = convert_to_date(row.get('Connector_Last_Login_Date_Time__c'))
        h_connector_last_update = convert_to_date(row.get('Connector_Last_Update_Date__c'))

        volunteer = Volunteer(
            first_name=row.get('FirstName'),
            last_name=row.get('LastName'),
            middle_name=None,  # Assuming 'middle_name' is not present in the CSV
            suffix=None,  # Assuming 'suffix' is not present in the CSV
            email=row.get('Email'),
            address=None,  # Assuming 'address' is not present in the CSV
            primary_phone=row.get('Phone'),
            secondary_phone=row.get('MobilePhone'),
            active=True,  # Assuming all entries are active
            birthday=None,  # Assuming 'birthday' is not present in the CSV
            connector_account_id=None,  # Assuming 'connector_account_id' is not present in the CSV
            gender=row.get('Gender__c'),
            contact_type=None,  # Assuming 'contact_type' is not present in the CSV
            do_not_call=convert_to_bool(row.get('DoNotCall')),
            h_salesforce_id=row.get('Id'),
            h_salesforce_account_id=row.get('AccountId'),
            secondary_email=row.get('npe01__AlternateEmail__c'),
            home_email=row.get('npe01__HomeEmail__c'),
            work_email=row.get('npe01__WorkEmail__c'),
            prefered_email=row.get('npe01__Preferred_Email__c'),
            country_code=row.get('OtherCountryCode'),
            city=row.get('MailingCity'),
            state=row.get('MailingState'),
            postal_code=row.get('MailingPostalCode'),
            preferred_phone=row.get('npe01__PreferredPhone__c'),
            h_owner_id=convert_to_int(row.get('OwnerId')),
            opt_out_email=convert_to_bool(row.get('HasOptedOutOfEmail')),
            opt_out_phone=convert_to_bool(row.get('DoNotCall')),
            h_created_date=h_created_date,
            h_salesforce_primary_aff=row.get('npsp__Primary_Affiliation__c'),
            h_org_name=row.get('organization_name'),
            age_group=row.get('Age_Group__c'),
            do_not_contact=convert_to_bool(row.get('npsp__Do_Not_Contact__c')),
            h_connector_join_date=h_connector_join_date,
            h_connector_last_login_date=h_connector_last_login_date,
            h_connecotr_join_date=h_connector_join_date,
            h_connector_id=convert_to_int(row.get('Connector_User_ID__c')),
            h_first_volunteer_date=h_first_volunteer_date,
            h_num_of_attended_sessions=convert_to_int(row.get('Number_of_Attended_Volunteer_Sessions__c')),
            h_num_of_noshow_sessions=convert_to_int(row.get('Number_of_No_Show_Volunteer_Sessions__c')),
            h_org_name_reported=row.get('Organization_self_reported__c'),
            person_of_color=convert_to_bool(row.get('Person_of_Color__c')),
            racial_ethnic_background=row.get('Racial_Ethnic_Background__c'),
            status=row.get('Volunteer_Status__c'),
            h_last_email_message=row.get('Last_Email_Message__c'),
            h_connector_last_update=h_connector_last_update,
            h_connector_signup_role=row.get('Connector_SignUp_Role__c'),
            h_last_completed_task=row.get('Last_Completed_Task__c'),
            connector_active_subscription=convert_to_bool(row.get('Connector_Active_Subscription__c')),
            created_at=datetime.now(),  # Assign current time as the created_at timestamp
            updated_at=datetime.now(),  # Assign current time as the updated_at timestamp
            deleted_at=None  # Assuming none are deleted
        )

        # Validate and clean email formats
        if pd.notna(volunteer.email) and "@" not in volunteer.email:
            volunteer.email = None

        # Validate and clean phone numbers
        if pd.notna(volunteer.primary_phone) and not volunteer.primary_phone.isdigit():
            volunteer.primary_phone = None
        if pd.notna(volunteer.secondary_phone) and not volunteer.secondary_phone.isdigit():
            volunteer.secondary_phone = None

        session.add(volunteer)
    except Exception as e:
        print(f"Error processing row {index}: {e}")

try:
    session.commit()
except Exception as e:
    print(f"Error during commit: {e}")
    session.rollback()
finally:
    session.close()
