"""module for user sign up and login"""
import psycopg2
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from . import cursor
from app.models.models import User
from app.utils import validate_signup
from app.utils import check_keys
from instance.config import conn


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

        # Check if passwords provided match
        password = user_details["password"]
        confirm_password = user_details["confirm-password"]
        if password != confirm_password:
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
        password = generate_password_hash(password, method="sha256")
        confirm_password = generate_password_hash(
            confirm_password, method="sha256")

        try:
            user = User(username, email, password, confirm_password)
            user.register_user(cursor)
            message = "user registered successfully"
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
        params = ['email', 'password']
        length = 2

        # Check provided fields
        if check_keys(user_details, params, length):
            return check_keys(user_details, params, length)

        email = user_details["email"]
        password = user_details["password"]

        # Check and log in user
        try:
            user = User.login_user(cursor, email, password)
        except (Exception, psycopg2.DatabaseError) as error:
            message = "incorrect username or password"
            response = jsonify({"login failed": message})
            response.status_code = 401
            return response

        if user:
            if check_password_hash(user["password"], password):
                # Grab user info for later user
                username = user["username"]
                user_id = user["user_id"]

                # create access token with username and id
                identity_dict = {'user_id': user_id, 'username': username}
                access_token = create_access_token(identity=identity_dict)

                # return responses
                message = "logged in as {}".format(username)
                response = jsonify(
                    {"success": message, "access_token": access_token})
                response.status_code = 200
                return response
            else:
                message = "incorrect username or password"
                response = jsonify({"login failed": message})
                response.status_code = 401
                return response
