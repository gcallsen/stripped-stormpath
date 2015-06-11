import json
import os
import logging, logging.config
import yaml
from flask import Flask
from flask.ext.mail import Mail
# from rhodb.database import db, cache_init_app
from flask.ext.stormpath import StormpathManager
from config import config
from flask.ext.sqlalchemy import SQLAlchemy

# Create uninitialized instances of the key extentions we use
# To be initialized in the create_app() application factory
#
mail = Mail()
stormpath_manager = StormpathManager()
db = SQLAlchemy()

def setup_logging(
    default_path='lib/logging-config.yaml',
    default_level=logging.INFO,
    custom_logging_config='CUSTOM_LOGGING_CONFIG'
):
    """ Setup logging configuration
        logging.config.dictConfig(yaml.load(open('lib/logging-config.yaml', 'r')))
    """
    logging_config_path = default_path
    custom_logging_path = os.getenv(custom_logging_config, None)
    if custom_logging_path:
        logging_config_path = custom_logging_path
    if os.path.exists(logging_config_path):
        with open(logging_config_path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def create_app(config_name):
    """ Create and configure our Flask application. Configuration pulled from
        configure.py. This method invoked by manage.py.
    """
    # Patch FLOAT_REPR since it is not exposed. This encodes all float values
    # to precision 3
    json.encoder.FLOAT_REPR = lambda o: format(o, '.3f')

    # Create and configure application. Default template directory will be in
    # apps/fantasy/templates. Other blueprints can define their own folder.
    #
    app = Flask(__name__, template_folder="apps/fantasy/templates")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Configure the database
    db.init_app(app)

    # Initialize the cache
    # cache_init_app(app)

    # Initialize flask-mail
    mail.init_app(app)

    # Use StormPath for user authentication.
    stormpath_manager.init_app(app)

    # Add the API
    from apps.fantasy import fantasy_bp
    app.register_blueprint(fantasy_bp)

    # Configure logging
    setup_logging()

    return app
