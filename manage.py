from flask_script import Manager
from flask import jsonify, request
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.utils import db, allowed_commands, slackhelper
from config import get_env

from app.actions.bot_actions import BotActions
from app.repositories.user_repo import UserRepo

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
	command_text = request.data.get('text').split(" ")
	response_body = {'text': 'I do not understand that command. `/rmw help` for available commands'}
	request_slack_id = request.data.get('user_id')
	
	slack_response = slackhelper.user_info(request_slack_id)
	
	current_user = UserRepo.find_by_slackid(request_slack_id)
	bot_actions = BotActions(current_user=current_user)

	if command_text[0] not in allowed_commands:
		response_body = {'text': 'Invalid Command'}
	elif slack_response['ok'] is True:
		# slack_user_info = slack_response['user']['profile']

		# These Commands Require A Ride ID
		if len(command_text) > 1 and int(command_text[1]) > 0:
			if command_text[0] == 'ride-info':
				response_body = bot_actions.get_ride_info(command_text[1])

			if command_text[0] == 'join-ride':
				response_body = bot_actions.join_ride(command_text[1])
		else:
			response_body = {'text': 'Missing Required Parameter `ride id` '}

		if len(command_text) == 1:
			if command_text[0] == 'show-rides':
				response_body = bot_actions.show_rides()

	else:
		response_body = {'text': 'Internal Application Error'}
	
	response = jsonify(response_body)
	response.status_code = 200
	return response


if __name__ == '__main__':
	manager.run()
