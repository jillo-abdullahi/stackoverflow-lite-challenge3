"""Utility functions to perform validations"""
import re
from flask import jsonify
from instance.config import conn

cursor = conn.cursor()


def validate_signup(args):
    """
    method to check keys for signup input fields
    """
    params = ['username', 'email', 'password', 'confirm']
    length = 4

    if check_keys(args, params, length):
        return check_keys(args, params, length)

    # Check if username is valid
    if validate_username(args):
        return validate_username(args)

    # Check if email is valid
    if validate_email(args):
        return validate_email(args)

    # Check password length
    if validate_password(args):
        return validate_password(args)


def validate_email(args):
    """Function to validate username"""
    if not re.match(r'^[a-zA-Z0-9_\-\.]{3,}@.*\.[a-z]{2,4}$', args["email"]):
        msg = "Please enter a valid email"
        response = jsonify({"error": msg})
        response.status_code = 400
        return response


def validate_username(args):
    """Function to validate username"""
    if not re.match(r'^[a-zA-Z0-9]{5,20}$', args["username"]):
        message = """Username should have
                between 5 and 20 characters and
                must contain letters or numbers only"""
        response = jsonify({"error": message})
        response.status_code = 400
        return response


def validate_password(args):
    """Function to check password length"""
    if not re.match(r'^[\w\W]{6,}$', args["password"]):
        msg = "Password should have at least 6 characters"
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


def fetch_one(query, item):
    """
    Method to fetch a specific value from db table based on
    query provided"""
    cursor.execute(query, [item])
    element = cursor.fetchone()
    return element
