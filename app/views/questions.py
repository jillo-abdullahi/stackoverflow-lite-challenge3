"""module for all things questions"""
import time
import psycopg2
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


from . import cursor, now
from app.models.models import Question, Answer
from app.utils import check_keys
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
                        response = jsonify(
                            {"error": "That question has already been asked. Please ask another."})
                        response.status_code = 400
                        return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get questions. {}".format(error)
        # Validation checks passed.

        # Get time
        current_time = time.localtime()

        current_user = get_jwt_identity()
        title = question_details["title"]
        description = question_details["description"]
        date_created = time.strftime("%d-%m-%Y %H:%M", current_time)
        user_id = current_user["user_id"]

        try:
            question = Question(title, description, date_created, user_id)
            question.post_question(cursor)

            response = jsonify({"message": "Question successfully posted"})
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
                response = jsonify({"message": "No questions yet"})
                response.status_code = 404
                return response
            response = jsonify({"questions": questions})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "failed to fetch all questions. {}".format(error)


class QuestionsByUserView(Resource):
    """
    Class to list questions by a specific user
    """
    @jwt_required
    def get(self, user_id):
        """
        get questions by a given user
        """
        try:
            questions = Question.get_questions_by_user(cursor, user_id)
            if not questions:
                response = jsonify(
                    {"message": "You haven't asked any questions yet"})
                response.status_code = 404
                return response
            response = jsonify({"questions": questions})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "failed to fetch question by user. {}".format(error)


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

            response = jsonify({"question": question})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                msg = "Sorry, question with that id does not exist."
                response = jsonify({"error": msg})
                response.status_code = 404
                return response

    @jwt_required
    def delete(self, qn_id):
        """
        Delete a question
        """

        current_user = get_jwt_identity()

        try:
            question = Question.get_one_question(cursor, qn_id)

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                msg = "Sorry, question with that Id does not exist"
                response = jsonify({"message": msg})
                response.status_code = 404
                return response

        try:
            # Check if current user owns question.
            if current_user["user_id"] == question["user_id"]:
                # Delete answers associated first
                Answer.delete_all_answers(cursor, qn_id)
                Question.delete_question(cursor, qn_id)
                response = jsonify(
                    {"message": "Question deleted successfully"})
                response.status_code = 200
                return response
            message = "You are not the author of this question"
            response = jsonify(
                {"message": message})
            response.status_code = 401
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                if(conn):
                    return "failed to fetch question by user. {}".format(error)
