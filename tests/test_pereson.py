import unittest
from app import app, db
from app.models.models import Person

class TestPersonModel(unittest.TestCase):

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

    def test_create_person(self):
        with app.app_context():
            person = Person(
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com'
            )
            db.session.add(person)
            db.session.commit()
            self.assertEqual(person.first_name, 'John')
            self.assertEqual(person.last_name, 'Doe')
            self.assertEqual(person.email, 'john.doe@example.com')

if __name__ == '__main__':
    unittest.main()
