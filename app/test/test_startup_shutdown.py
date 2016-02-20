import unittest
from flask import current_app
from app import db, create_app

class StartShutdownTestCase(unittest.TestCase):
    # Defines what to be run at the beginning of each test
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # First test. Tests must begin with "test_"
    def test_correct_runmode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_existance(self):
        self.assertTrue(current_app is not None)

    # Define action to take at end of test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


