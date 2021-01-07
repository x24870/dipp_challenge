"""
Module for managing Flask app's init functions
"""
import os

from flask import Flask
from config.config import ConfigName, get_config

from app.controllers.index import bp_index
from app.controllers.image import bp_image


def create_app():
    """
    Method to init and set up the Flask application
    """
    flask_app = Flask(import_name="dipp_app")

    _init_config(flask_app)
    _register_blueprint(flask_app)
    _register_api_error(flask_app)

    return flask_app


def _init_config(app):
    """
    Method to initialize the configuration
    """
    env = os.getenv("FLASK_ENV", ConfigName.DEV.value)
    app.config.from_object(get_config(env))


def _register_blueprint(app):
    """
    Method to register the blueprint
    """
    prefix = app.config["API_BASE_PATH"]

    app.register_blueprint(bp_index, url_prefix=prefix)
    app.register_blueprint(bp_image, url_prefix=prefix)


def _register_api_error(app):
    """
    Method to register the api error
    """
    pass
