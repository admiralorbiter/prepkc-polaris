import unittest
from app import app, db
from app.models import Student, School

class TestStudentModel(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Create a school instance as it's required for Student
            self.school = School(name='Central High School', district='Central District', level='High')
            db.session.add(self.school)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_student(self):
        with app.app_context():
            # Re-query the school instance to ensure it's attached to the session
            school = School.query.filter_by(name='Central High School').first()
            student = Student(
                first_name='John',
                last_name='Smith',
                email='john.smith@example.com',
                primary_affiliation_id=school.id
            )
            db.session.add(student)
            db.session.commit()
            self.assertEqual(student.first_name, 'John')
            self.assertEqual(student.last_name, 'Smith')
            self.assertEqual(student.email, 'john.smith@example.com')
            self.assertEqual(student.primary_affiliation_id, school.id)

if __name__ == '__main__':
    unittest.main()
