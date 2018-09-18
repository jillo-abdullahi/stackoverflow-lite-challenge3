"""Configurations for various environments"""
import os
import psycopg2

# Connect to db based on environment
if os.getenv('APP_SETTINGS') == 'testing':
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_TEST_URL'))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

elif os.getenv('APP_SETTINGS') == 'development':
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)


class Config(object):
    """Configuration for parent class"""
    DEBUG = False
    TESTING = False


class Production(object):
    """Class for production"""


class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Conficuration for testing"""
    DEBUG = True
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': Production
}
