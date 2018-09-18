"""Module for app entry point"""
import os
from flask_restful import Api
from app import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

api = Api(app)


if __name__ == '__main__':
    app.run()
