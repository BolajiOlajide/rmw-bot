import time
from calendar import timegm
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app.utils.slackhelper import SlackHelper

db = SQLAlchemy()
slackhelper = SlackHelper()

allowed_commands = [
    "add-ride",
    "show-rides",
    "ride-info",
    "join-ride",
    "leave-ride",
    "cancel-ride",
    "help",
]


def timestamp_to_epoch(timestamp):
    utc_time = time.strptime(
        timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return timegm(utc_time)


def convert_time_to_timestamp(time_string):
    today = datetime.today()
    time_string = time_string.split(":")
    time_string[1] = "59" if int(time_string[1]) > 59 else time_string[1]
    full_time_string = "{} {}, {} {}:{}".format(
        today.day, today.month, today.year, time_string[0], time_string[1]
    )
    return datetime.strptime(full_time_string, "%d %m, %Y %H:%M")


def check_ride_status(ride):
    if ride.status == 0:
        return "INACTIVE"
    return "ACTIVE"


elements = [
    {
        "label": "Pickup Point",
        "type": "text",
        "name": "origin",
        "placeholder": "Your Pickup Location",
        "hint": "Enter an address or landmark to setup as your pickup location",
    },
    {
        "label": "Drop-off Point",
        "type": "text",
        "name": "destination",
        "placeholder": "Your Drop off Point/Destination",
        "hint": "Enter a destination address of landmark",
    },
    {
        "label": "Take-off time",
        "type": "text",
        "name": "take_off",
        "placeholder": "Time of Departure",
        "hint": "Enter the time you will take in this formats - {08:00}, {20:00}",
    },
    {
        "label": "Number of Riders needed",
        "type": "text",
        "name": "max_seats",
        "subtype": "number",
        "placeholder": "Number of spaces available",
        "hint": "Add the number of spaces available on your ride e.g. 2",
    },
]
