"""Test module for user login"""

import unittest
import json

from app import create_app
from instance.config import conn


class TestUserCanLogin(unittest.TestCase):
    """
    Class to test endpoint for user login
    """

    def setUp(self):
        """
        set up method to start test_client and initialize variables
        """
        self.app = create_app("development")
        self.app = self.app.test_client()

        self. new_user_details = {
            "username": "jillWoche",
            "email": "jayloabdullahi@gmail.com",
            "password": "johndoe95",
            "confirm-password": "johndoe95"
        }

        self.user_login_details = {
            "email": "jayloabdullahi@gmail.com",
            "password": "johndoe95"
        }

    def test_user_can_login(self):
        """
        Method to test if the user can log in
        """
        register_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )
        self.assertEqual(register_response.status_code, 201)

        # Login user
        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.user_login_details),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)

        # Test message
        message = json.loads(response.data)['success']
        self.assertIn('logged in as', message)

    def test_incorrect_email(self):
        """
        Method to test login using incorrect email
        """
        # Set incorrect email

        self.user_login_details["email"] = "wrong.email@gmail.com"

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.user_login_details),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        # Test message
        message = json.loads(response.data)['login failed']
        self.assertEqual(message, "incorrect username or password")

    def test_incorrect_password(self):
        """Method to test login using incorrect password"""
        self.user_login_details["password"] = "wrongpassword123"

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.user_login_details),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        # Test message
        message = json.loads(response.data)['login failed']
        self.assertEqual(message, "incorrect username or password")

    def tearDown(self):
        """
        Clear table values after running tests
        """
        cursor = conn.cursor()
        query_user = """ DELETE FROM users """
        query_questions = """ DELETE FROM questions """
        query_answers = """ DELETE FROM answers """
        reset_users = """ ALTER SEQUENCE users_id_seq RESTART WITH 1 """
        cursor.execute(reset_users)
        cursor.execute(query_answers)
        cursor.execute(query_questions)
        cursor.execute(query_user)
        conn.commit()
