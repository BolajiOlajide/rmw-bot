from flask_sqlalchemy import SQLAlchemy
from app.utils.slackhelper import SlackHelper
import time
from datetime import datetime
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


def convert_time_to_timestamp(time_string):
	today = datetime.today()
	time_string = time_string.split(':')
	time_string[1] = '59' if int(time_string[1]) > 59 else time_string[1]
	full_time_string = '{} {}, {} {}:{}'.format(
		today.day, today.month, today.year, time_string[0], time_string[1])
	return datetime.strptime(full_time_string, '%d %m, %Y %H:%M')


def check_ride_status(ride):
	if ride.status == 0:
		ride_status = 'INACTIVE'
	elif ride.status == 1:
		ride_status = 'ACTIVE'
	return ride_status
