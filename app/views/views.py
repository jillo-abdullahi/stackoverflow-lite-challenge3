"""Module for user sign up and login"""
import os
import datetime
import psycopg2
from flask import Flask, request, jsonify
from flask_restful import Resource, Api


from instance.config import app_config
from app.models.models import Question
from app.utilities import validate_question
from instance.config import conn

config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.url_map.strict_slashes = False
api = Api(app)


cursor = conn.cursor()
now = datetime.datetime.now()


class QuestionsPostGet(Resource):
    """Resource class for posting and getting all questions """

    def post(self):
        """
        Post a question
        """
        question_details = request.get_json()

        # Validate question fields
        if validate_question(question_details):
            return validate_question(question_details)

        # Check if question has already been asked

        try:
            questions = Question.get_all_questions(cursor)
            if questions:
                for question in questions:
                    if question["title"] == question_details["title"]:
                        response = jsonify({"Error": "Question already asked"})
                        response.status_code = 400
                        return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed to get questions. {}".format(error)
        # Validation checks passed.

        title = question_details["title"]
        description = question_details["description"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))
        user_id = 1

        try:
            question = Question(title, description, date_created, user_id)
            question.post_question(cursor)

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed to insert record. {}".format(error)

        response = jsonify({"message": "Question successfully posted"})
        response.status_code = 201
        return response

    def get(self):
        """
        Get all questions
        """
        questions = Question.get_all_questions(cursor)
        if not questions:
            response = jsonify({"message": "No questions yet"})
            response.status_code = 404
            return response
        response = jsonify({"Questions": questions})
        response.status_code = 200
        return response


api.add_resource(QuestionsPostGet, '/stackoverflowlite/api/v1/questions')
