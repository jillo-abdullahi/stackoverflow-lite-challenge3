"""Module for all things answers"""
import psycopg2
import time
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import cursor, now
from app.models.models import Question, Answer
from app.utils import check_keys
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
        current_time = time.localtime()
        current_user = get_jwt_identity()
        description = answer_details["description"]
        date_created = time.strftime("%d-%m-%Y %H:%M", current_time)
        user_id = current_user["user_id"]

        try:
            Question.get_one_question(cursor, qn_id)

            answer = Answer(description, date_created, user_id, qn_id)
            answer.post_answer(cursor)
            response = jsonify({"message": "Answer posted successfully"})
            response.status_code = 201
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                msg = "Sorry, question with that id does not exist"
                response = jsonify({"error": msg})
                response.status_code = 404
                return response

    @jwt_required
    def get(self, user_id):
        """
        Get all answers posted by a user
        """
        try:
            answers = Answer.get_answers_by_user(cursor, user_id)
            if not answers:
                message = "You haven't answered any questions yet"
                response = jsonify({"message": message})
                response.status_code = 404
                return response
            response = jsonify({"Answers": answers})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get answers. {}".format(error)


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
        if not answer_author:
            msg = "Sorry, answer with that id does not exist."
            response = jsonify({"error": msg})
            response.status_code = 404
            return response

        question_author = Question.get_question_author(cursor, qn_id)
        if not question_author:
            msg = "Sorry, question with that id does not exist."
            response = jsonify({"error": msg})
            response.status_code = 404
            return response
        answer_details = request.get_json()

        # Updating answer
        try:
            if bool(answer_details):
                # check input
                params = ["description"]
                length = 1

                if check_keys(answer_details, params, length):
                    return check_keys(answer_details, params, length)

                if user_id == answer_author[0]:
                    answer_details = request.get_json()

                    description = answer_details["description"]
                    Answer.update_answer(cursor, description, ans_id)

                    message = "Answer successfully updated"
                    response = jsonify({"message": message})
                    response.status_code = 200
                    return response
                else:
                    message = "Non-author: you cannot update this answer"
                    response = jsonify({"message": message})
                    response.status_code = 403
                    return response
            else:
                if user_id == question_author[0]:
                    Answer.accept_answer(cursor, ans_id)
                    message = "Answer status successfully updated"
                    response = jsonify({"message": message})
                    response.status_code = 200
                    return response
                else:
                    message = "Non-author: you did not author this question to accept answer"
                    response = jsonify({"message": message})
                    response.status_code = 403
                    return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to update answer. {}".format(error)


class AnswersByUserView(Resource):
    """
    Class to get all answers posted by a given user
    """
    @jwt_required
    def get(self, user_id):
        """
        Get all answers by a given user
        """
        try:
            answers = Answer.get_answers_by_user(cursor, user_id)
            if not answers:
                message = "you have not answered any questions yet"
                response = jsonify({"message": message})
                response.status_code = 404
                return response
            response = jsonify({"message": answers})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to update answer. {}".format(error)


class AnswerDescriptionView(Resource):
    """
    Class to get description for a specific answer
    """
    @jwt_required
    def get(self, ans_id):
        """
        Get description for a specific answer
        """
        try:
            description = Answer.get_answer_title(cursor, ans_id)
            if not description:
                message = "answer was not found"
                response = jsonify({"message": message})
                response.status_code = 404
                return response
            response = jsonify({"message": description})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get answer description. {}".format(error)

    @jwt_required
    def delete(self, ans_id):
        """
        Delete a specific answer
        """
        try:
            if Answer.delete_answer(cursor, ans_id):
                msg = "Answer successfully deleted"
                response = jsonify({"message": msg})
                response.status_code = 200
                return response
            else:
                message = "Answer with that id does not exist"
                response = jsonify({"message": message})
                response.status_code = 404
                return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to delete answer. {}".format(error)
