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
	currenttime = datetime.now().time().strftime("%H:%M")
	if currenttime >= "10:00" and currenttime <= "13:00":
		if time_string >= "10:00" and time_string >= "12:00":
			time_string = ("%s%s" % (time_string, " AM"))
		else:
			time_string = ("%s%s" % (time_string, " PM"))
	else:
		time_string = ("%s%s" % (time_string, " PM"))
	time_string = datetime.strptime(time_string, '%I:%M %p')
	time_string = time_string.strftime("%H:%M %p")
	# m2 = m2[:-3]
	# time_string = time.mktime(datetime.strptime(time_string, '%I:%M %p'))
	# new_time = time.mktime(datetime.datetime.strptime(time_string, "%H:%M").timetuple())
	return time_string


def check_ride_status(ride):
	if ride.status == 0:
		ride_status = 'INACTIVE'
	elif ride.status == 1:
		ride_status = 'ACTIVE'
	return ride_status
