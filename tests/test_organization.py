import unittest
from app import app, db
from app.models import Organization

class TestOrganizationModel(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_organization(self):
        with app.app_context():
            organization = Organization(
                name='Helping Hands'
            )
            db.session.add(organization)
            db.session.commit()
            self.assertEqual(organization.name, 'Helping Hands')

if __name__ == '__main__':
    unittest.main()
