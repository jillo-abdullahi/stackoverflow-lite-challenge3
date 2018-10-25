"""Test module for posting/updating of answers"""

import unittest
import json

from app import create_app
from instance.config import conn


class TestAnswers(unittest.TestCase):
    """
    Class to test answers endpoints
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

        self.answer_user = {
            "username": "ChoChang",
            "email": "cho.chang@gmail.com",
            "password": "john123456",
            "confirm": "john123456"
        }

        self.answer_user_login = {
            "email": "cho.chang@gmail.com",
            "password": "john123456"
        }

        self.user_login_details = {
            "email": "hermione.granger@gmail.com",
            "password": "john123456"
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

        self.question_details = {
            "title": "How to exit Vim on Ubuntu 16.04",
            "description": "How does one get the exit Vim from terminal?"
        }

        self.answer_details = {
            "description": "Type Ctrl+O to exit"
        }
        self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            headers={
                "Authorization": self.access_token,
                "content-type": "application/json"})

    def test_answer_non_existent_question(self):
        """
        Test when answer description has not been provided
        """
        # Try to post an answer for non-existing question
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/55/answers',
            data=json.dumps(self.answer_details),
            headers={
                "Authorization": self.access_token,
                "content-type": 'application/json'})

        self.assertEqual(response.status_code, 404)

        # Test message
        message = json.loads(response.get_data(as_text=True))[
            'error']
        self.assertEqual(
            message, "Sorry, question with that id does not exist")

    def test_answer_description_not_provided(self):
        """
        Test for answer description not provided
        """
        self.answer_details["description"] = " "

        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/1/answers',
            data=json.dumps(self.answer_details),
            headers={
                "Authorization": self.access_token,
                "content-type": 'application/json'})

        self.assertEqual(response.status_code, 400)

        # Test message
        message = json.loads(response.get_data(as_text=True))[
            'error']
        self.assertEqual(message, "description must not be empty")

    def test_user_can_post_answer(self):
        """
        Test if user can answer someone else's question
        """

        # Register and login as different user
        self.app.post(
            '/stackoverflowlite/api/v1/auth/signup',
            data=json.dumps(self.answer_user),
            content_type='application/json'
        )

        login_response = self.app.post(
            '/stackoverflowlite/api/v1/auth/login',
            data=json.dumps(self.answer_user_login),
            content_type='application/json'
        )

        token = json.loads(login_response.data.decode())[
            "access_token"]
        access_token = "Bearer {}".format(token)

        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/1/answers',
            data=json.dumps(self.answer_details),
            headers={
                "Authorization": access_token,
                "content-type": 'application/json'})

        self.assertEqual(response.status_code, 201)

        # Test message
        message = json.loads(response.get_data(as_text=True))[
            'message']
        self.assertEqual(message, "Answer posted successfully")

    def test_user_can_delete_answer(self):
        """
        Test if user can delete their answer
        """

        # Try to post an answer to a question
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/1/answers',
            data=json.dumps(self.answer_details),
            headers={
                "Authorization": self.access_token,
                "content-type": 'application/json'})

        self.assertEqual(response.status_code, 201)

        # Try to delete answer
        del_response = self.app.delete(
            '/stackoverflowlite/api/v1/answer/1',
            headers={
                "Authorization": self.access_token,
                "content-type": 'application/json'})

        self.assertEqual(del_response.status_code, 200)

        # Test Message
        message = json.loads(del_response.get_data(as_text=True))[
            'message']
        self.assertEqual(message, "Answer successfully deleted")

        # Attempt to delete question as well

        quest_response = self.app.delete(
            '/stackoverflowlite/api/v1/questions/1',
            headers={
                "Authorization": self.access_token, "content-type": "application/json"})
        # Test response
        self.assertEqual(quest_response.status_code, 200)

    def test_delete_question_with_answers(self):
        """
        Test if a question with answers can be deleted
        """
        # Try to post an answer to a question
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/1/answers',
            data=json.dumps(self.answer_details),
            headers={
                "Authorization": self.access_token,
                "content-type": 'application/json'})

        self.assertEqual(response.status_code, 201)

        # Try to delete the question
        quest_response = self.app.delete(
            '/stackoverflowlite/api/v1/questions/1',
            headers={
                "Authorization": self.access_token, "content-type": "application/json"})
        # Test response
        self.assertEqual(quest_response.status_code, 200)

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
