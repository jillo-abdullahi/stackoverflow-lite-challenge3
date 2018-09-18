"""Module for all things answers"""
import psycopg2
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import cursor, now
from app.models.models import Question, Answer
from app.utilities import check_keys
from instance.config import conn


class AnswersView(Resource):
    """
    Class for posting of answers
    """
    @jwt_required
    def post(self, qn_id):
        """
        post a question
        """
        answer_details = request.get_json()

        # Validate answer fields before posting
        params = ['description']
        length = 1

        # Check provided fields
        if check_keys(answer_details, params, length):
            return check_keys(answer_details, params, length)

        # post answer
        current_user = get_jwt_identity()
        description = answer_details["description"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))
        user_id = current_user["user_id"]
        question_author = Question.get_question_author(cursor, qn_id)

        try:

            question = Question.get_one_question(cursor, qn_id)
            if not question:
                response = jsonify({"error": "question doesn't exist"})
                response.status_code = 404
                return response

            # Check if user can answer their own question
            if user_id != question_author[0]:
                answer = Answer(description, date_created, user_id, qn_id)
                answer.post_answer(cursor)

                response = jsonify({"message": "answer successfully posted"})
                response.status_code = 201
                return response
            else:
                message = "you cannot answer your own question"
                response = jsonify({"message": message})
                response.status_code = 403
                return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to post answer. {}".format(error)


class AnswerView(Resource):
    """
    Class to choose preferred answer or update answer
    """
    @jwt_required
    def put(self, qn_id, ans_id):
        """
        update answer or choose as preferred
        """
        current_user = get_jwt_identity()
        user_id = current_user["user_id"]
        answer_author = Answer.get_answer_author(cursor, ans_id)
        question_author = Question.get_question_author(cursor, qn_id)

        # Updating answer
        try:
            if user_id == answer_author[0]:
                answer_details = request.get_json()

                params = ["description"]
                length = 1

                if check_keys(answer_details, params, length):
                    return check_keys(answer_details, params, length)

                description = answer_details["description"]

                Answer.update_answer(cursor, description, ans_id)
                message = "answer successfully updated"
                response = jsonify({"message": message})
                response.status_code = 200
                return response
            else:
                message = "non-author: you cannot update this answer"
                response = jsonify({"message": message})
                response.status_code = 403
                return response

            if user_id == question_author[0]:
                Answer.accept_answer(cursor, ans_id)
                message = "answer status successfully updated"
                response = jsonify({"message": message})
                response.status_code = 200
                return response
            else:
                message = "non-author: you did not author this question to accept answer"
                response = jsonify({"message": message})
                response.status_code = 403
                return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to update answer. {}".format(error)
