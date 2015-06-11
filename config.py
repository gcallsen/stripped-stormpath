import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Primary configuration variables requried application-wide on any environ
    """

    # Set the current Application and API Versions.
    # They should be consistent with the git version number.
    APP_VERSION = 'v0.0.1'
    API_VERSION = 'v0.0.1'

    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'foobar'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PARENT_API_KEY = os.environ.get('PARENT_API_KEY') or '1234'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or "Pit Rho <no-reply@pitrho.com>"
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'none'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'none'
    FANTASY_MAIL_SUBJECT_PREFIX = '[Pit Rho]'

    STORMPATH_API_KEY_ID = os.environ.get('STORMPATH_API_KEY_ID')
    STORMPATH_API_KEY_SECRET = os.environ.get('STORMPATH_API_KEY_SECRET')
    STORMPATH_APPLICATION = os.environ.get('STORMPATH_APPLICATION')
    STORMPATH_ENABLE_GIVEN_NAME = True
    STORMPATH_REQUIRE_GIVEN_NAME = True
    STORMPATH_ENABLE_MIDDLE_NAME = False
    STORMPATH_ENABLE_SURNAME = True
    STORMPATH_REQUIRE_SURNAME = False
    STORMPATH_ENABLE_USERNAME = False
    STORMPATH_ENABLE_FORGOT_PASSWORD = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ Establish development-specific variables
    """

    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """ Establish testing-specific variables
    """

    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """ Establish production-specific variables
    """
    DEBUG = False
    TESTING = False

# Expose our 'config' dictionary keyed off of configuration kind name
# 'default' value is DevelopmentConfig
#
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
