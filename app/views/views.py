"""Module for user sign up and login"""
import os
import datetime
import psycopg2
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended import create_access_token, get_jwt_identity


from instance.config import app_config
from app.models.models import Question, Answer, User
from app.utilities import validate_question, validate_answer, validate_signup
from app.utilities import validate_username, validate_email, validate_password
from app.utilities import validate_login
from instance.config import conn

config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__, instance_relative_config=True)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
app.config.from_object(app_config[config_name])
app.url_map.strict_slashes = False


jwt = JWTManager(app)
api = Api(app)


cursor = conn.cursor()
now = datetime.datetime.now()


class UserSignup(Resource):
    """
    Class for user signup
    """

    def post(self):
        """
        Add new user
        """
        user_details = request.get_json()

        # Check if all required fields have been provided
        if validate_signup(user_details):
            return validate_signup(user_details)

        # Check if username is valid
        if not validate_username(user_details):
            msg1 = "username should have "
            msg2 = "between 5 and 20 characters and "
            msg3 = "must contain letters or numbers only"
            response = jsonify({"error": msg1 + msg2 + msg3})
            response.status_code = 400
            return response

        # Check if email is valid
        if not validate_email(user_details):
            msg = "invalid email"
            response = jsonify({"error": msg})
            response.status_code = 400
            return response

        # Check password length
        if not validate_password(user_details):
            msg = "password must have at least 6 characters"
            response = jsonify({"error": msg})
            response.status_code = 400
            return response

        # Check if passwords provided match
        password = generate_password_hash(user_details["password"])
        confirm_password = user_details["confirm-password"]
        if not check_password_hash(password, confirm_password):
            msg = "passwords provided do not match"
            response = jsonify({"error": msg})
            response.status_code = 400
            return response

        # Check if username or email have been taken
        try:
            users = User.get_users(cursor)
            if users:
                for user in users:
                    if user["username"] == user_details["username"]:
                        message = "username has already been taken"
                        response = jsonify({"error": message})
                        response.status_code = 400
                        return response

                    if user["email"] == user_details["email"]:
                        message = "email has already been registered"
                        response = jsonify({"error": message})
                        response.status_code = 400
                        return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get users. {}".format(error)

        # All validations passed. Add user
        username = user_details["username"]
        email = user_details["email"]
        confirm_password = generate_password_hash(
            user_details["confirm-password"])

        try:
            user = User(username, email, password, confirm_password)
            user.register_user(cursor)
            message = "User registered successfully"
            response = jsonify({"message": message})
            response.status_code = 201
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to add user. {}".format(error)


class UserLogin(Resource):
    """Class for user sign in"""

    def post(self):
        """
        login user
        """
        user_details = request.get_json()

        # Validate login details provided
        if validate_login(user_details):
            return validate_login(user_details)

        email = user_details["email"]
        password = user_details["password"]

        # Check and log in user
        try:
            users = User.get_users(cursor)
            if users:
                for user in users:
                    check_pass = check_password_hash(
                        user["password"], password)
                    if email != user["email"] or not check_pass:
                        message = "incorrect username or password"
                        response = jsonify({"login failed": message})
                        response.status_code = 401
                        return response

                    # Grab user info for later user
                    username = user["username"]
                    user_id = user["user_id"]

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to get users. {}".format(error)

        # create access token with username and id
        identity_dict = {'user_id': user_id, 'username': username}
        access_token = create_access_token(identity=identity_dict)

        # return responses
        message = "Logged in as {}".format(username)
        response = jsonify({"success": message, "access_token": access_token})
        response.status_code = 200
        return response


class QuestionsView(Resource):
    """Resource class for posting and getting all questions """
    @jwt_required
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
        try:
            question = Question.get_one_question(cursor, qn_id)
            if not question:
                response = jsonify({"error": "question doesn't exist"})
                response.status_code = 404
                return response
            Question.delete_question(cursor, qn_id)
            response = jsonify({"message": "question deleted successfully"})
            response.status_code = 200
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to delete question. {}".format(error)


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

        if validate_answer(answer_details):
            return validate_answer(answer_details)

        # post answer
        current_user = get_jwt_identity()
        description = answer_details["description"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))
        user_id = current_user["user_id"]

        try:
            question = Question.get_one_question(cursor, qn_id)
            if not question:
                response = jsonify({"error": "question doesn't exist"})
                response.status_code = 404
                return response

            answer = Answer(description, date_created, user_id, qn_id)
            answer.post_answer(cursor)

            response = jsonify({"message": "Answer successfully posted"})
            response.status_code = 201
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            if(conn):
                return "Failed to post answer. {}".format(error)


api.add_resource(QuestionsView, '/stackoverflowlite/api/v1/questions')
api.add_resource(QuestionView,
                 '/stackoverflowlite/api/v1/questions/<int:qn_id>')
api.add_resource(
    AnswersView, '/stackoverflowlite/api/v1/questions/<int:qn_id>/answers')
api.add_resource(
    UserSignup, '/stackoverflowlite/api/v1/auth/signup')
api.add_resource(
    UserLogin, '/stackoverflowlite/api/v1/auth/login')
