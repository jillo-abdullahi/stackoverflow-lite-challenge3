"""Module for app entry point"""
import os
from flask_restful import Api
from app import create_app
from migrations import migration

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

api = Api(app)

# Create tables
migration()


if __name__ == '__main__':
    app.run()
