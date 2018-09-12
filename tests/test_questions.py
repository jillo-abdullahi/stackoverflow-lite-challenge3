# Test module for questions"""

import unittest
import json

from app.views.views import app
from instance.config import conn


class TestQuestions(unittest.TestCase):
    """
    Class to test endpoints relating to questions
    """

    def setUp(self):
        """
        set up method to start test_client and initialize variables
        """
        self.app = app.test_client()

        self.question_details = {
            "title": "How to exit Vim on Ubuntu",
            "description": "How does one exit from terminal?"}

    def test_user_can_post_question(self):
        """
        Method to test if a new question can be added
        """
        response = self.app.post(
            '/stackoverflowlite/api/v1/questions',
            data=json.dumps(self.question_details),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        # Test message
        message = json.loads(response.get_data(as_text=True))[
            'message']
        self.assertEqual(message, 'Question added successfully')

    def test_user_can_get_all_questions(self):
        """
        Method to test if user can get all questions
        """

        # Attempt to get all questions
        get_response = self.app.get('/stackoverflowlite/api/v1/questions',
                                    headers={
                                        "content-type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

    def test_user_can_get_specific_question(self):
        """
        Method to test if a user can get a specific question
        """

        # Attempt to get specific question
        get_response = self.app.get('/stackoverflowlite/api/v1/questions/1',
                                    headers={
                                        "content-type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

    def test_user_can_delete_question(self):
        """
        Method to test if user can delete a question
        """
        response = self.app.delete('/stackoverflowlite/api/v1/questions/1',
                                   headers={
                                       "content-type": "application/json"})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """
        Clear table values after running tests
        """
        cursor = conn.cursor()
        query = """ DELETE FROM questions """
        cursor.execute(query)
