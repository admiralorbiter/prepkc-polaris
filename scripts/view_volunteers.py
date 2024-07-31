from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Person, Volunteer

# Database setup
engine = create_engine('sqlite:///volunteers.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Query all volunteers
volunteers = session.query(Person, Volunteer).join(Volunteer, Person.id == Volunteer.id).all()

if not volunteers:
    print("No data found in the volunteers table.")
else:
    for person, volunteer in volunteers:
        print(f"Volunteer - ID: {volunteer.id}, Name: {person.first_name} {person.last_name}, Email: {person.email}")
