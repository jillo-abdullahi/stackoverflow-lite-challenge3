import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


from instance.config import app_config
from app.views.auth import UserSignup, UserLogin, UserView
from app.views.questions import QuestionsView, QuestionView
from app.views.questions import QuestionsByUserView
from app.views.answers import AnswerView, AnswersView
from app.views.answers import AnswersByUserView, AnswerDescriptionView


def create_app(config_name):
    """
    Method to instantiate app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['DATABASE_URI'] = os.environ['DATABASE_URL']
    jwt = JWTManager(app)
    CORS(app)

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
    api.add_resource(
        UserView, '/stackoverflowlite/api/v1/auth/users/<username>')

    # Add routes for questions
    api.add_resource(QuestionsView, '/stackoverflowlite/api/v1/questions')
    api.add_resource(QuestionView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>')
    api.add_resource(QuestionsByUserView,
                     '/stackoverflowlite/api/v1/question/<int:user_id>')

    # Add routes for answers
    api.add_resource(AnswersView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>/answers')
    api.add_resource(AnswerView,
                     '/stackoverflowlite/api/v1/questions/<int:qn_id>/answers/<int:ans_id>')
    api.add_resource(AnswersByUserView,
                     '/stackoverflowlite/api/v1/answers/<int:user_id>')
    api.add_resource(AnswerDescriptionView,
                     '/stackoverflowlite/api/v1/answer/<int:ans_id>')

    return app
