import csv
from app import app, db  # Adjust the import according to your project structure
from app.models import Volunteer  # Adjust the import according to your project structure

def import_jobs(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            volunteer = Volunteer(
                name=row['Name'],
                email=row['npe01__HomeEmail__c'],
                affiliation=row['npsp__Primary_Affiliation__r.Name'],
                job_category=row['Job Category'],
                skills_text=row['Volunteer_Skills_Text__c'],
                skills=row['Volunteer_Skills__c']
            )
            db.session.add(volunteer)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():  # Ensures that the entire script runs within an application context
        db.create_all()  # Create tables based on the models defined
        csv_file_path = 'jobs.csv'  # Update this to the path of your CSV file
        import_jobs(csv_file_path)
        print('Jobs data has been successfully imported into the database.')
    