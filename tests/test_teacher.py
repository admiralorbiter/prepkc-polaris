import unittest
from app import app, db
from app.models import Teacher, School

class TestTeacherModel(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Create a school instance as it's required for Teacher
            self.school = School(name='Central High School', district='Central District', level='High')
            db.session.add(self.school)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_teacher(self):
        with app.app_context():
            # Re-query the school instance to ensure it's attached to the session
            school = School.query.filter_by(name='Central High School').first()
            teacher = Teacher(
                first_name='Jane',
                last_name='Doe',
                email='jane.doe@example.com',
                primary_affiliation_id=school.id,
                type='Math'
            )
            db.session.add(teacher)
            db.session.commit()
            self.assertEqual(teacher.first_name, 'Jane')
            self.assertEqual(teacher.last_name, 'Doe')
            self.assertEqual(teacher.email, 'jane.doe@example.com')
            self.assertEqual(teacher.primary_affiliation_id, school.id)
            self.assertEqual(teacher.type, 'Math')

if __name__ == '__main__':
    unittest.main()
