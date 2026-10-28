import unittest
from app import app, init_db, get_db

class SmartEventSystemTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        init_db()

    def test_01_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smart Event Management System', response.data)

    def test_02_events_page(self):
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upcoming College Events', response.data)
        self.assertIn(b'CodeCraft', response.data)

    def test_03_student_login(self):
        response = self.client.post('/login', data={
            'email': 'student@college.edu',
            'password': 'Student@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Registered Events', response.data)

    def test_04_admin_login_and_dashboard(self):
        response = self.client.post('/login', data={
            'email': 'admin@college.edu',
            'password': 'Admin@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Console', response.data)
        self.assertIn(b'Add New Event', response.data)

    def test_05_event_registration_and_duplicate_prevention(self):
        # 1. Login student
        self.client.post('/login', data={
            'email': 'student@college.edu',
            'password': 'Student@123'
        })

        # 2. Register for event 1
        res = self.client.post('/event/1/register', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'successfully registered', res.data)

        # 3. Attempt duplicate registration for event 1
        res_dup = self.client.post('/event/1/register', follow_redirects=True)
        self.assertIn(b'already registered for this event', res_dup.data)

if __name__ == '__main__':
    unittest.main()
