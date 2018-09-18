"""Test module for user signup"""
import psycopg2
import unittest
import json

from app import create_app
from instance.config import conn


class TestUserCanSignup(unittest.TestCase):
    """Class to test for user ability to register"""

    def setUp(self):
        """
        set up method to start test_client and initialize variables
        """
        self.app = create_app("testing")
        self.app = self.app.test_client()

        self. new_user_details = {
            "username": "HermGranger",
            "email": "hermione.granger@gmail.com",
            "password": "john123456",
            "confirm-password": "john123456"
        }

    def test_invalid_email(self):
        """
        Method to test for bad user email
        """

        # Set invalid email
        self.new_user_details["email"] = "jillojay@gmail"

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)['error']
        self.assertEqual(message, 'please enter valid email')

    def test_empty_username(self):
        """
        Method to test for empty username field
        """

        # Set empty username
        self.new_user_details["username"] = " "

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)['error']
        self.assertIn('must not be empty', message)

    def test_invalid_username(self):
        """
        Method to test for invalid username
        """

        # Set invalid username
        self.new_user_details["username"] = "j%$%"

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)['error']
        self.assertIn('must contain letters or numbers only', message)

    def test_missing_keys(self):
        """
        Method to test for missing keys
        """

        # Delete password key
        del self.new_user_details["password"]

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)['error']
        self.assertIn('please provide your password', message)

    def test_password_length(self):
        """
        Method to test for correct password length
        """
        # Set password to less than 6 characters
        self.new_user_details["password"] = "chek1"

        self.new_user_details["confirm-password"] = "check1"

        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)['error']
        self.assertEqual(message, 'password must have at least 6 characters')

    def test_existing_username(self):
        """
        Method to test if user can register twice
        """
        self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Register user again
        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertEqual(message, 'username has already been taken')

    def test_user_can_signup(self):
        """
        Method to test if user can register
        """
        response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        # Test response
        self.assertEqual(response.status_code, 201)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(message, 'user registered successfully')

    def tearDown(self):
        """
        Clear values in db after tests have run
        """
        try:
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

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to execute queries. {}".format(error)
