import unittest
from datetime import date, time
from app import app, db
from app.models.models import Session

class TestSessionModel(unittest.TestCase):

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

    def test_create_session(self):
        with app.app_context():
            session = Session(
                name='Session 1',
                type='Workshop',
                status='Active',
                start_date=date(2024, 7, 30),
                start_time=time(9, 0),
                end_time=time(17, 0),
                volunteers_needed=5
            )
            db.session.add(session)
            db.session.commit()
            self.assertEqual(session.name, 'Session 1')
            self.assertEqual(session.type, 'Workshop')
            self.assertEqual(session.status, 'Active')
            self.assertEqual(session.start_date, date(2024, 7, 30))
            self.assertEqual(session.start_time, time(9, 0))
            self.assertEqual(session.end_time, time(17, 0))
            self.assertEqual(session.volunteers_needed, 5)

if __name__ == '__main__':
    unittest.main()

