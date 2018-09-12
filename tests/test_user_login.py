"""Test module for user login"""

import unittest
import json

from app.views.views import app
from instance.config import conn


class TestUserCanLogin(unittest.TestCase):
    """
    Class to test endpoint for user login
    """

    def setUp(self):
        """
        set up method to start test_client and initialize variables
        """
        self.app = app.test_client()

        self. new_user_details = {
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "johndoe95",
            "confirm-password": "johndoe95"
        }

        self.user_login_details = {
            "email": "john.doe@gmail.com",
            "password": "johndoe95"}

    def test_user_can_login(self):
        """
        Method to test if the use can log in
        """
        # Register user first
        register_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )
        self.assertEqual(register_response.status_code, 201)

        # Login user
        login_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signin',
            data=json.dumps(self.user_login_details),
            content_type='application/json')

        self.assertEqual(login_response.status_code, 200)

        # Test message
        message = json.loads(login_response.get_data(as_text=True))['message']
        self.assertEqual(message, 'User login successful')

    def tearDown(self):
        """
        Clear table values after running tests
        """
        cursor = conn.cursor()
        query = """ DELETE FROM users """
        cursor.execute(query)
