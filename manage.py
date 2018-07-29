from flask_script import Manager
from flask import jsonify, request, make_response
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


@app.route('/', methods=['GET', 'POST'])
def home():
	response = jsonify({'YOU': 'Are Awesome!'})
	response.status_code = 200
	return response


@app.route('/bot', methods=['POST', 'GET', 'PATCH'])
def bot():
	command_text = request.data.get('text').split(" ")
	response_body = {'text': 'I do not understand that command. `/rmw help` for available commands'}
	request_slack_id = request.data.get('user_id')
	message_trigger = request.data.get('trigger_id')

	slack_response = slackhelper.user_info(request_slack_id)

	current_user = UserRepo.find_by_slackid(request_slack_id)
	bot_actions = BotActions(current_user=current_user)

	if command_text[0] not in allowed_commands:
		response_body = {'text': 'Invalid Command'}

	elif slack_response['ok'] is True:
		if len(command_text) == 1:
			if command_text[0] == 'show-rides':
				response_body = bot_actions.show_rides()

			if command_text[0] == 'add-ride':
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
		# These Commands Require A Ride ID
		elif len(command_text) > 1 and int(command_text[1]) > 0:
			if command_text[0] == 'ride-info':
				response_body = bot_actions.get_ride_info(command_text[1])

			if command_text[0] == 'join-ride':
				response_body = bot_actions.join_ride(command_text[1])

			if command_text[0] == 'cancel-ride':
				response_body = bot_actions.cancel_ride(command_text[1])
		else:
			response_body = {'text': 'Missing Required Parameter `ride id` '}


	else:
		response_body = {'text': 'Internal Application Error'}

	response = jsonify(response_body)
	response.status_code = 200
	return response


@app.route('/interactive', methods=['POST', 'GET'])
def interactive():
	request_payload = json.loads(request.data.get('payload'))
	webhook_url = request_payload["response_url"]

	slack_user_info = slackhelper.user_info(request_payload['user']['id'])
	user_data = slack_user_info['user']

	current_user = UserRepo.find_or_create(by='slack_uid', value=request_payload["user"]["id"], user_data=user_data)

	bot_actions = BotActions(current_user=current_user)

	if request_payload["type"] == "dialog_submission":
		slack_data = bot_actions.add_ride(
			origin=request_payload["submission"]["origin"],
			destination=request_payload["submission"]["destination"],
			take_off=request_payload["submission"]["take_off"],
			max_seats=request_payload["submission"]["max_seats"])

		response = requests.post(
			webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)

		if response.status_code != 200:
			if slack_data["errors"]:
				response = jsonify(slack_data)
				response.status_code = 200
				return response
			else:
				raise ValueError(
					'Request to slack returned an error %s, the response is:\n%s'
					% (response.status_code, response.text)
				)

	elif request_payload["type"] == "dialog_cancellation":
		slack_data = {'text': "We hope you change your mind and share a ride"}
		response = requests.post(
			webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)
		if response.status_code != 200:
			raise ValueError(
				'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)

	return "", 200


if __name__ == '__main__':
	manager.run()
