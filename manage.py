import json
from threading import Thread

import requests
from flask import jsonify, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.actions.bot_actions import BotActions
from app.repositories.user_repo import UserRepo
from app.utils import allowed_commands, db, slackhelper
from app.utils.handle_bot_actions import handle_bot_actions
from config import get_env

app = create_app(get_env("APP_ENV"))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

help_message = """The following commands are available on the RideMyWay platform
>>>
:heavy_plus_sign: *Add a ride* `/rmw add-ride` _This is used to add a ride to the system.
This option is only available to drivers._

:bow_and_arrow: *Show Rides* `/rmw show-rides` _This is used to view all recent rides in the system._

:information_source: *Get Ride Info* `/rmw ride-info <ride_id>` _Get details of a ride_

:juggling: *Join a Ride* - `/rmw join-ride <ride_id>` _Join a ride using the ride ID_

:walking: *Leave a ride* - `/rmw leave-ride <ride_id>` _Join a ride using the ride ID_

:mailbox_closed: *Cancel a ride* - `/rmw cancel-ride <ride_id>` _Cancel a ride using the ride ID_

:speaking_head_in_silhouette: *Help* - `/rmw help` _Display RMW help menu_
"""


@app.route("/", methods=["GET", "POST"])
def home():
    msg = {"status": "success"}
    response = jsonify(msg)
    response.status_code = 200
    return response


@app.route("/bot", methods=["POST", "GET", "PATCH"])
def bot():
    command_text = request.data.get("text").split(" ")
    request_slack_id = request.data.get("user_id")
    webhook_url = request.data.get("response_url")
    message_trigger = request.data.get("trigger_id")

    if command_text[0] == "help" or (not command_text[0]):
        response_body = {"text": help_message}
        response = jsonify(response_body)
        response.status_code = 200
        return response

    if command_text[0] not in allowed_commands:
        response_body = {"text": "Invalid Command. Use the `/rmw help` to get help."}
        response = jsonify(response_body)
        response.status_code = 200
        return response

    rmw_thread = Thread(
        target=handle_bot_actions,
        args=(app, message_trigger, webhook_url, request_slack_id, command_text),
    )
    rmw_thread.start()
    return "", 200


@app.route("/interactive", methods=["POST", "GET"])
def interactive():
    request_payload = json.loads(request.data.get("payload"))
    webhook_url = request_payload["response_url"]

    slack_user_info = slackhelper.user_info(request_payload["user"]["id"])
    user_data = slack_user_info["user"]

    current_user = UserRepo.find_or_create(
        by="slack_uid", value=request_payload["user"]["id"], user_data=user_data
    )

    bot_actions = BotActions(current_user=current_user)
    check_for_error = True

    if request_payload["type"] == "dialog_submission":
        slack_data = bot_actions.add_ride(
            origin=request_payload["submission"]["origin"],
            destination=request_payload["submission"]["destination"],
            take_off=request_payload["submission"]["take_off"],
            max_seats=request_payload["submission"]["max_seats"],
        )

    elif request_payload["type"] == "dialog_cancellation":
        slack_data = {
            "text": "We hope you change your mind and help others share a ride"
        }
        check_for_error = False

    slackhelper.send_delayed_msg(webhook_url, slack_data, check_for_error)
    return "", 200


if __name__ == "__main__":
    manager.run()
