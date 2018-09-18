"""module for all things questions"""

import psycopg2
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


from . import cursor, now
from app.models.models import Question, Answer
from app.utilities import check_keys
from instance.config import conn


class QuestionsView(Resource):
    """
    Resource class for posting and getting all questions
    """
    @jwt_required
    def post(self):
        """
        Post a question
        """
        question_details = request.get_json()

        # Validate question fields
        params = ['title', 'description']
        length = 2

        # Check provided fields
        if check_keys(question_details, params, length):
            return check_keys(question_details, params, length)

        # Check if question has already been asked
        try:
            questions = Question.get_all_questions(cursor)
            if questions:
                for question in questions:
                    if question["title"] == question_details["title"]:
                        response = jsonify({"error": "question already asked"})
                        response.status_code = 400
                        return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get questions. {}".format(error)
        # Validation checks passed.

        current_user = get_jwt_identity()
        title = question_details["title"]
        description = question_details["description"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))
        user_id = current_user["user_id"]

        try:
            question = Question(title, description, date_created, user_id)
            question.post_question(cursor)

            response = jsonify({"message": "question successfully posted"})
            response.status_code = 201
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                conn.rollback()
                return "Failed to insert record. {}".format(error)

    @jwt_required
    def get(self):
        """
        Get all questions
        """
        try:
            questions = Question.get_all_questions(cursor)
            if not questions:
                response = jsonify({"message": "no questions yet"})
                response.status_code = 404
                return response
            response = jsonify({"questions": questions})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "failed to fetch questions. {}".format(error)


class QuestionView(Resource):
    """
    Class to get one question as well as delete
    """
    @jwt_required
    def get(self, qn_id):
        """
        get a specific question"""
        try:
            question = Question.get_one_question(cursor, qn_id)
            if not question:
                response = jsonify({"error": "question doesn't exist"})
                response.status_code = 404
                return response

            response = jsonify({"question": question})
            response.status_code = 200
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to fetch question. {}".format(error)

    @jwt_required
    def delete(self, qn_id):
        """
        Delete a question
        """

        current_user = get_jwt_identity()
        try:
            question = Question.get_one_question(cursor, qn_id)
            if not question:
                response = jsonify({"error": "question doesn't exist"})
                response.status_code = 404
                return response

            # Check if current user owns question.

            if current_user["user_id"] == question["user_id"]:
                # Delete answers associated first
                Answer.delete_answer(cursor, qn_id)
                Question.delete_question(cursor, qn_id)
                response = jsonify(
                    {"message": "question deleted successfully"})
                response.status_code = 200
                return response
            message = "You are not the author of this question"
            response = jsonify(
                {"message": message})
            response.status_code = 401
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to delete question. {}".format(error)