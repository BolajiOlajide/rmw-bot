from flask_sqlalchemy import SQLAlchemy
from app.utils.slackhelper import SlackHelper
import time, datetime
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
	currenttime = datetime.datetime.now().time().strftime("%H:%M")
	if currenttime >= "10:00" and currenttime <= "13:00":
		if m2 >= "10:00" and m2 >= "12:00":
			m2 = ("""%s%s""" % (m2, " AM"))
		else:
			m2 = ("""%s%s""" % (m2, " PM"))
	else:
		m2 = ("""%s%s""" % (m2, " PM"))
	# m2 = datetime.datetime.strptime(m2, '%I:%M %p')
	# m2 = m2.strftime("%H:%M %p")
	# m2 = m2[:-3]
	m2 = time.mktime(datetime.datetime.strptime(m2, '%I:%M %p').timetuple())
	# new_time = time.mktime(datetime.datetime.strptime(s, "%H:%M").timetuple())
	return m2

def check_ride_status(ride):
	if ride.status == 0:
		 ride_status = 'INACTIVE'
	elif ride.status == 1:
		ride_status = 'ACTIVE'
	return ride_status