from flask_api import FlaskAPI
from config.env import app_env
from app.utils import db
from flask import jsonify
import json


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(app_env[config_name])
    app.config.from_pyfile('../config/env.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from . import models
    db.init_app(app)

    return app
