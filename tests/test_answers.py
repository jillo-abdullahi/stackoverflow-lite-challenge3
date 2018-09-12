"""Test module for posting/updating of answers"""

import unittest
import json

from app.views.views import app
from instance.config import conn


class TestAnswers(unittest.TestCase):
    """
    Class to test answers endpoints
    """

    def setUp(self):
        """
       set up method to start test_client and initialize variables
        """
        self.app = app.test_client()

        self.question_details = {
            "title": "How to exit Vim on Ubuntu 16.04",
            "description": "How does one get the exit Vim from terminal?"
        }
        self.answer_details = {
            "description": "Type Ctrl+O to exit"
        }
        self.new_answer = {"description": "Try googling"}

    def test_user_can_add_answer(self):
        """
        Method to test if user can add an answer
        """
        # Post a question first
        question_response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            content_type='application/json')

        self.assertEqual(question_response.status_code, 201)

        # Try to post an answer
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions/1/answers',
            data=json.dumps(self.answer_details),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)

        # Test message
        message = json.loads(response.get_data(as_text=True))[
            'message']
        self.assertEqual(message, 'Answer successfully posted')

    def test_user_can_accept_answer(self):
        """
        Method to test if user can mark an answer as preferred
        Or update an answer.
        """
        resp = self.app.put('/stackoverflowlite/api/v1/questions/1/answers/1',
                            data=json.dumps(self.new_answer),
                            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        """
        Clear table values after running tests
        """
        cursor = conn.cursor()
        query = """ DELETE FROM answers """
        cursor.execute(query)
