from flask_api import FlaskAPI

from app.utils import db
from config.env import app_env


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(app_env[config_name])
    app.config.from_pyfile("../config/env.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from . import models  # noqa: #F401

    db.init_app(app)

    return app
