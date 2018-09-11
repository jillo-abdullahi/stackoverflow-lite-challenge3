"""Configurations for various environments"""


class Config(object):
    """Configuration for parent class"""
    DEBUG = False
    TESTING = False


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
    'testing': TestConfig
}
