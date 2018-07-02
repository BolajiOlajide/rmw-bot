from flask_sqlalchemy import SQLAlchemy
from app.utils.slackhelper import SlackHelper


db = SQLAlchemy()
slackhelper = SlackHelper()

allowed_commands = [
    'add-ride'
]
