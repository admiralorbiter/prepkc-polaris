import unittest
from app import app, db
from app.models.models import School

class TestSchoolModel(unittest.TestCase):

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

    def test_create_school(self):
        with app.app_context():
            school = School(
                name='Central High School',
                district='Central District',
                level='High'
            )
            db.session.add(school)
            db.session.commit()
            self.assertEqual(school.name, 'Central High School')
            self.assertEqual(school.district, 'Central District')
            self.assertEqual(school.level, 'High')

if __name__ == '__main__':
    unittest.main()
