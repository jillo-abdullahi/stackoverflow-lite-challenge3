"""File for app set up"""

from flask import Flask
from flask_restful import Resource, Api

from instance.config import app_config


def create_app(config_name):
    """Function to set up app"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False

    return app
