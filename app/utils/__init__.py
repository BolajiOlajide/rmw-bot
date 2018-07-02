from flask_sqlalchemy import SQLAlchemy
from app.utils.slackhelper import SlackHelper
import time
from calendar import timegm

db = SQLAlchemy()
slackhelper = SlackHelper()

allowed_commands = [
	'add-ride',
	'show-rides',
	'ride-info',
	'join-ride',
	'leave-ride',
	'cancel-ride',
	'help'
]


def timestamp_to_epoch(timestamp):
	utc_time = time.strptime(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ")
	return timegm(utc_time)
