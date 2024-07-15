from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Volunteer

# Function to convert string to datetime with multiple formats
def convert_to_datetime(value):
    if pd.isnull(value):
        return None
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%Y %H:%M',
        '%m/%d/%Y, %I:%M %p',
        '%m/%d/%y %I:%M %p'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{value}' does not match any of the known formats")

# Function to handle multiple date values in a single string
def handle_multiple_dates(value):
    if pd.isnull(value):
        return None
    date_strings = value.split('; ')
    dates = [convert_to_datetime(date_string) for date_string in date_strings]
    return dates[-1]  # Use the last date in the list

# Database connection setup (replace with your actual connection string)
DATABASE_URI = 'sqlite:///polaris.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Load the Volunteer CSV file
volunteer_file_path = 'Volunteer.csv'
volunteer_data = pd.read_csv(volunteer_file_path)

# Mapping dictionary
field_mapping = {
    'SalesforceID': 'h_salesforce_id',
    'SalesforceAccountID': 'h_salesforce_account_id',
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
    'Connector_Last_Login_Date_Time__c': 'h_connector_last_login_date',
    'Connector_User_ID__c': 'h_connector_id',
    'First_Volunteer_Date__c': 'h_first_volunteer_date',
    'Number_of_Attended_Volunteer_Sessions__c': 'h_num_of_attended_sessions',
    'Number_of_No_Show_Volunteer_Sessions__c': 'h_num_of_noshow_sessions',
    'Organization_self_reported__c': 'h_org_name_reported',
    'Person_of_Color__c': 'person_of_color',
    'Racial_Ethnic_Background__c': 'racial_ethnic_background',
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
    'npe01__PreferredPhone__c': 'preferred_phone',
    'Title': 'title',
    'Connector_Active_Subscription__c': 'connector_active_subscription',
    'Gender__c': 'gender',
    'Highest_Level_of_Educational__c': 'education_background',
    'Last_Mailchimp_Email_Date__c': 'last_mailchimp_email_date',
    'Last_Volunteer_Date__c': 'last_volunteer_date',
}

# Drop unnecessary columns
volunteer_data.drop(columns=['MobilePhone', 'HomePhone', 'npe01__WorkPhone__c', 'Type_of_Sessions_Participated_In__c'], inplace=True)

# Rename columns according to the mapping
volunteer_data.rename(columns=field_mapping, inplace=True)

# Convert date and datetime fields to Python datetime objects
date_fields = [
    'h_created_date', 'h_connector_join_date', 'h_connector_last_login_date',
    'h_first_volunteer_date', 'h_last_email_message', 'h_connector_last_update', 'h_last_completed_task'
]

for field in date_fields:
    volunteer_data[field] = volunteer_data[field].apply(handle_multiple_dates)

# Replace NaN values in integer fields with 0
integer_fields = ['h_num_of_attended_sessions', 'h_num_of_noshow_sessions']
for field in integer_fields:
    volunteer_data[field] = volunteer_data[field].fillna(0).astype(int)

# Define the list of fields that match the Volunteer model
volunteer_fields = {
    'h_salesforce_id', 'h_salesforce_account_id', 'secondary_email', 'home_email', 'work_email', 'prefered_email',
    'country_code', 'city', 'state', 'postal_code', 'primary_phone', 'h_owner_id', 'opt_out_email', 'do_not_call',
    'h_created_date', 'h_salesforce_primary_aff', 'h_org_name', 'age_group', 'do_not_contact', 'h_connector_join_date',
    'h_connector_last_login_date', 'h_connector_id', 'h_first_volunteer_date', 'h_num_of_attended_sessions',
    'h_num_of_noshow_sessions', 'h_org_name_reported', 'person_of_color', 'racial_ethnic_background', 'h_interests',
    'h_skills_text', 'h_skills', 'status', 'h_last_email_message', 'h_connector_last_update', 'h_connector_signup_role',
    'h_last_completed_task', 'suffix', 'first_name', 'last_name', 'email', 'preferred_phone', 'title',
    'connector_active_subscription', 'gender', 'education_background', 'last_mailchimp_email_date', 'last_volunteer_date'
}

# Convert DataFrame to list of dictionaries and filter out unnecessary fields
volunteer_records = volunteer_data.to_dict(orient='records')
filtered_records = [{k: v for k, v in record.items() if k in volunteer_fields} for record in volunteer_records]

# Insert records into the database
for record in filtered_records:
    volunteer = Volunteer(**record)
    session.add(volunteer)

session.commit()
print("Data imported successfully.")
