"""Utility functions to perform validations"""
import re
from flask import jsonify


def validate_email(args):
    """Function to validate username"""
    if not re.match(r'^[a-zA-Z0-9_\-\.]{3,}@.*\.[a-z]{2,4}$', args["email"]):
        msg = "please enter valid email"
        response = jsonify({"error": msg})
        response.status_code = 400
        return response


def validate_username(args):
    """Function to validate username"""
    if not re.match(r'^[a-zA-Z0-9]{5,20}$', args["username"]):
        msg1 = "username should have "
        msg2 = "between 5 and 20 characters and "
        msg3 = "must contain letters or numbers only"
        response = jsonify({"error": msg1 + msg2 + msg3})
        response.status_code = 400
        return response


def validate_password(args):
    """Function to check password length"""
    if not re.match(r'^[\w\W]{6,}$', args["password"]):
        msg = "password must have at least 6 characters"
        response = jsonify({"error": msg})
        response.status_code = 400
        return response


# General utility function
def check_keys(args, params, length):
    """Function to check if dict keys and values"""

    # Check if required keys have been provided
    for key in params:
        if key not in args:
            response = jsonify(
                {"error": "please provide your {}".format(key)})
            response.status_code = 400
            return response

    # check if values provided are empty
    for key in args:
        if not args[key].strip():
            response = jsonify(
                {"error": "{} must not be empty".format(key)})
            response.status_code = 400
            return response

    # Check if correct number of fields provided
    if len(args) != length:
        response = jsonify(
            {"error": "Fields required: {}".format(", ".join(params))})
        response.status_code = 400
        return response
