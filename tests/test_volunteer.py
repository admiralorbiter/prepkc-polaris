import unittest
from app import app, db
from app.models import Volunteer, Organization

class TestVolunteerModel(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Create an organization instance as it's required for Volunteer
            self.organization = Organization(name='Helping Hands')
            db.session.add(self.organization)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_volunteer(self):
        with app.app_context():
            # Re-query the organization instance to ensure it's attached to the session
            organization = Organization.query.filter_by(name='Helping Hands').first()
            volunteer = Volunteer(
                first_name='Emily',
                last_name='Brown',
                email='emily.brown@example.com',
                primary_affiliation_id=organization.id
            )
            db.session.add(volunteer)
            db.session.commit()
            self.assertEqual(volunteer.first_name, 'Emily')
            self.assertEqual(volunteer.last_name, 'Brown')
            self.assertEqual(volunteer.email, 'emily.brown@example.com')
            self.assertEqual(volunteer.primary_affiliation_id, organization.id)

if __name__ == '__main__':
    unittest.main()
