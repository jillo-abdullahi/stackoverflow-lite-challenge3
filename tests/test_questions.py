# Test module for questions"""
import unittest
import json

from app import create_app
from instance.config import conn


class TestQuestions(unittest.TestCase):
    """
    Class to test endpoints relating to questions
    """

    def setUp(self):
        """
        set up method to start test_client and initialize variables
        """
        self.app = create_app("testing")
        self.app = self.app.test_client()

        self.new_user_details = {
            "username": "HermGranger",
            "email": "hermione.granger@gmail.com",
            "password": "john123456",
            "confirm": "john123456"
        }

        self.user_login_details = {
            "email": "hermione.granger@gmail.com",
            "password": "john123456"
        }

        self.non_author_details = {
            "username": "ChoChang",
            "email": "cho.chang@gmail.com",
            "password": "cho123456",
            "confirm": "cho123456"
        }

        self.non_author_login = {
            "email": "cho.chang@gmail.com",
            "password": "cho123456"
        }

        self.question_details = {
            "title": "How to exit Vim on Ubuntu",
            "description": "How does one exit from terminal?"
        }
        self.register_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.new_user_details),
            content_type='application/json'
        )

        self.login_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.user_login_details),
            content_type='application/json'
        )

        self.token = json.loads(self.login_response.data.decode())[
            "access_token"]
        self.access_token = "Bearer {}".format(self.token)

    def test_user_can_post_question(self):
        """
        Method to test if a new question can be added
        """
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 201)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(message, 'Question successfully posted')

    def test_user_can_get_all_questions(self):
        """
        Method to test if user can get all questions
        """

        # Post question first
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Attempt to get all questions
        get_response = self.app.get('/stackoverflowlite/api/v1/questions',
                                    headers={
                                        "Authorization": self.access_token,
                                        "content-type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

    def test_user_can_get_specific_question(self):
        """
        Method to test if a user can get a specific question
        """

        # Post question first
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Attempt to get specific question
        get_response = self.app.get('/stackoverflowlite/api/v1/questions/1',
                                    headers={
                                        "Authorization": self.access_token,
                                        "content-type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

    def test_user_can_delete_question(self):
        """
        Method to test if user can delete a question
        """
        # Post question first
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        response = self.app.delete('/stackoverflowlite/api/v1/questions/1',
                                   headers={
                                       "Authorization": self.access_token,
                                       "content-type": "application/json"})
        # Test response
        self.assertEqual(response.status_code, 200)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(message, 'Question deleted successfully')

    def test_delete_non_existing_question(self):
        """
        Test if a non-existent question can be deleted
        """
        response = self.app.delete('/stackoverflowlite/api/v1/questions/22',
                                   headers={
                                       "Authorization": self.access_token,
                                       "content-type": "application/json"})
        # Test response
        self.assertEqual(response.status_code, 404)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(
            message, "Sorry, question with that Id does not exist")

    def test_if_non_author_can_delete_question(self):
        """
        Test if a non-author can delete a question
        """

        # Register, login and register token for non-author
        self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.non_author_details),
            content_type='application/json'
        )

        non_auth_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.non_author_login),
            content_type='application/json'
        )

        token = json.loads(non_auth_response.data.decode())[
            "access_token"]
        access_token = "Bearer {}".format(token)

        # Post a question
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": access_token,
                "content-type": "application/json"})

        # Attempt to delete question with non-author token

        response = self.app.delete('/stackoverflowlite/api/v1/questions/1',
                                   headers={
                                       "Authorization": self.access_token,
                                       "content-type": "application/json"})
        # Test response
        self.assertEqual(response.status_code, 401)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(message, "You are not the author of this question")

    def test_for_duplicate_question(self):
        """
        Test if the same question can be asked twice
        """

        # Posting once
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Posting twice
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertEqual(
            message, "That question has already been asked. Please ask another.")

    def test_getting_if_no_questions_exist(self):
        """
        Test response on getting questions when none has been asked
        """
        # Attempt to get all questions
        response = self.app.get('/stackoverflowlite/api/v1/questions',
                                headers={
                                    "Authorization": self.access_token,
                                    "content-type": "application/json"})
        # Test response
        self.assertEqual(response.status_code, 404)

        # Test message
        message = json.loads(response.data)[
            'message']
        self.assertEqual(message, "No questions yet")

    def test_empty_question_title(self):
        """
        Test if question title is empty
        """

        # Set empty title
        self.question_details["title"] = " "

        # Post question with empty title

        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertIn("must not be empty", message)

    def test_empty_question_description(self):
        """
        Test if question title is empty
        """

        # Set empty title
        self.question_details["description"] = " "

        # Post question with empty title
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertIn("must not be empty", message)

    def test_missing_question_key(self):
        """
        Test if a question key has not been provided
        """

        # Remove description key
        del self.question_details["description"]

        # Post question with missing description key
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertEqual(message, "please provide your description")

    def test_extra_key_added(self):
        """
        Test if a user adds their own key
        """

        # Adding an extra key
        self.question_details["new_key"] = "new key"

        # Post question with new key
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

        # Test response
        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.data)[
            'error']
        self.assertIn("Fields required:", message)

    def tearDown(self):
        """
        Clear values in db after tests have run
        """
        cursor = conn.cursor()
        answers_query = "DELETE FROM answers;"
        questions_query = "DELETE FROM questions;"
        users_query = "DELETE FROM users;"
        reset_users = "ALTER SEQUENCE users_id_seq RESTART WITH 1;"
        reset_questions = "ALTER SEQUENCE questions_id_seq RESTART WITH 1;"
        reset_answers = "ALTER SEQUENCE answers_id_seq RESTART WITH 1;"
        cursor.execute(reset_answers)
        cursor.execute(reset_questions)
        cursor.execute(reset_users)
        cursor.execute(answers_query)
        cursor.execute(questions_query)
        cursor.execute(users_query)

        conn.commit()
