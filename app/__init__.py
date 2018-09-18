import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config
from app.views.auth import UserSignup, UserLogin
from app.views.questions import QuestionsView, QuestionView
from app.views.answers import AnswerView, AnswersView


def create_app(config_name):
    """
    Method to instantiate app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    jwt = JWTManager(app)

    api = Api(app)

    @app.route('/', methods=['GET'])
    @app.route('/favicon.ico', methods=['GET'])
    def api_documentation():
        """route for API documentation"""
        return render_template('version1.html')

    # Add routes for users
    api.add_resource(
        UserSignup, '/stackoverflowlite/api/v1/auth/signup')
    api.add_resource(
        UserLogin, '/stackoverflowlite/api/v1/auth/login')

    # Add routes for questions
    api.add_resource(QuestionsView, '/stackoverflowlite/api/v1/questions')
    api.add_resource(QuestionView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>')

    # Add routes for answers
    api.add_resource(AnswersView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>/answers')
    api.add_resource(AnswerView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>/answers/<int:ans_id>')

    return app
