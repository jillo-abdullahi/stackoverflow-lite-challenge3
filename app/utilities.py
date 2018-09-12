"""Utility functions to perform validations"""
from flask import jsonify


def validate_login(args):
    """Function to validate user provided fields for login"""
    params = ['email', 'password']
    length = 2

    # Check provided fields
    if check_keys(args, params, length):
        return check_keys(args, params, length)


def validate_signup(args):
    """Function to validate user-provided info when signing up"""
    params = ['username', 'email', 'password', 'confirm-password']
    length = 4

    # Check fields provided
    if check_keys(args, params, length):
        return check_keys(args, params, length)


def validate_question(args):
    """Function to validate question"""
    params = ['title', 'description']
    length = 2

    # Check provided fields
    return check_keys(args, params, length)


def validate_answer(args):
    """Function to validate answer"""
    params = ['description']
    length = 1

    # Check provided fields
    if check_keys(args, params, length):
        return check_keys(args, params, length)


# General utility function
def check_keys(args, params, length):
    """Function to check if dict keys and values"""

    # Check if required keys have been provided
    for key in params:
        if key not in args:
            response = jsonify(
                {"Error": "Please provide your {}".format(key)})
            response.status_code = 400
            return response

    # check if values provided are empty
    for key in args:
        if not args[key].strip():
            response = jsonify(
                {"Error": "{} must not be empty".format(key)})
            response.status_code = 400
            return response

    # Check if correct number of fields provided
    if len(args) != length:
        response = jsonify(
            {"Error": "Fields required: {}".format(", ".join(params))})
        response.status_code = 400
        return response
