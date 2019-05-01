from flask_script import Manager
from flask import jsonify, request
from flask_migrate import Migrate, MigrateCommand
import requests
import json
from app import create_app
from app.utils import db, allowed_commands, slackhelper
from config import get_env

from app.actions.bot_actions import BotActions
from app.repositories.user_repo import UserRepo

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

element = [
	{
		"label": "Pickup Point",
		"type": "text",
		"name": "origin",
		"placeholder": "Your Pickup Location",
		"hint": "Enter an address or landmark to setup as your pickup location"
	},
	{
		"label": "Drop-off Point",
		"type": "text",
		"name": "destination",
		"placeholder": "Your Drop off Point/Destination",
		"hint": "Enter a destination address of landmark"
	},
	{
		"label": "Take-off time",
		"type": "text",
		"name": "take_off",
		"placeholder": "Time of Departure",
		"hint": "Enter the time you will take in this formats - {08:00}, {20:00}"
	},
	{
		"label": "Number of Riders needed",
		"type": "text",
		"name": "max_seats",
		"subtype": "number",
		"placeholder": "Number of spaces available",
		"hint": "Add the number of spaces available on your ride e.g. 2"
	}
]

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


@app.route('/', methods=['GET', 'POST'])
def home():
	msg = { 'status': 'success' }
	response = jsonify(msg)
	response.status_code = 200
	return response


@app.route('/bot', methods=['POST', 'GET', 'PATCH'])
def bot():
	command_text = request.data.get('text').split(" ")
	request_slack_id = request.data.get('user_id')
	webhook_url = request.data.get('response_url')

	if (command_text[0] == 'help'):
		response_body = {'text': help_message}
		response = jsonify(response_body)
		response.status_code = 200
		slackhelper.send_delayed_msg(webhook_url, response_body)
		return response

	intro_message = f"""
Hey <@{request_slack_id}>,

I'm currently processing your request. Give me a minute and I'll be back with a response.
:smile:
"""
	response_body = {'text': intro_message}
	response = jsonify(response_body)
	response.status_code = 200
	slackhelper.send_delayed_msg(webhook_url, response_body)

	response_body = {'text': 'I do not understand that command. `/rmw help` for available commands'}
	message_trigger = request.data.get('trigger_id')

	slack_response = slackhelper.user_info(request_slack_id)

	current_user = UserRepo.find_by_slackid(request_slack_id)
	bot_actions = BotActions(current_user=current_user)

	if command_text[0] not in allowed_commands:
		response_body = {'text': 'Invalid Command. Use the `/rmw help` to get help.'}

	elif slack_response['ok']:
		if len(command_text) == 1:
			if command_text[0] == 'show-rides':
				response_body = bot_actions.show_rides()

			elif command_text[0] == 'add-ride':
				dialog = {
					"title": "Add A Ride",
					"submit_label": "Add",
					"callback_id": slack_response['user']['id'] + "_add_ride",
					"notify_on_cancel": True,
					"elements": element
				}
				slackhelper.dialog(dialog, message_trigger)
				msg = ':pencil: We are saving your ride...'
				response_body = {'text': msg}

			else:
				response_body = {'text': help_message}

		# These Commands Require A Ride ID
		elif len(command_text) > 1 and int(command_text[1]) > 0:
			if command_text[0] == 'ride-info':
				response_body = bot_actions.get_ride_info(command_text[1])
			elif command_text[0] == 'join-ride':
				response_body = bot_actions.join_ride(command_text[1])
			elif command_text[0] == 'cancel-ride':
				response_body = bot_actions.cancel_ride(command_text[1])
			elif command_text[0] == 'leave-ride':
				response_body = bot_actions.leave_ride(command_text[1])
		else:
			response_body = {'text': 'Missing Required Parameter `ride id` '}
	else:
		response_body = {'text': 'An error occurred. Contact the admin.'}

	response = jsonify(response_body)
	response.status_code = 200
	slackhelper.send_delayed_msg(webhook_url, response_body)
	return response


@app.route('/interactive', methods=['POST', 'GET'])
def interactive():
	request_payload = json.loads(request.data.get('payload'))
	webhook_url = request_payload["response_url"]

	slack_user_info = slackhelper.user_info(request_payload['user']['id'])
	user_data = slack_user_info['user']

	current_user = UserRepo.find_or_create(
		by='slack_uid', value=request_payload["user"]["id"],
		user_data=user_data
	)

	bot_actions = BotActions(current_user=current_user)
	check_for_error = True

	if request_payload["type"] == "dialog_submission":
		slack_data = bot_actions.add_ride(
			origin=request_payload["submission"]["origin"],
			destination=request_payload["submission"]["destination"],
			take_off=request_payload["submission"]["take_off"],
			max_seats=request_payload["submission"]["max_seats"]
		)

	elif request_payload["type"] == "dialog_cancellation":
		slack_data = {'text': "We hope you change your mind and share a ride"}
		check_for_error = False

	slackhelper.send_delayed_msg(webhook_url, slack_data, check_for_error)
	return "", 200


if __name__ == '__main__':
	manager.run()
