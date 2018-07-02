from flask_script import Manager
from flask import jsonify, request
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.utils import db, allowed_commands, slackhelper
from config import get_env

from app.actions.bot_actions import BotActions


app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
	command_text = request.data.get('text').split(" ")
	response_body = {'text': 'I do not understand that command. `/rmw help` for available commands'}
	request_slack_id = request.data.get('user_id')
	bot_actions = BotActions()
	
	slack_response = slackhelper.user_info(request_slack_id)
	
	if command_text[0] not in allowed_commands:
		response_body = {'text': 'Invalid Command'}

	if slack_response['ok'] is True:
		slack_user_info = slack_response['user']['profile']
		
		if command_text[0] == 'add-ride':
			response_body = {
				'status': 'success',
				'msg': bot_actions.add_ride()
			}
		
		if command_text[0] == 'ride-info':
			if len(command_text) > 1 and int(command_text[1]) > 0:
				response_body = bot_actions.get_ride_info(command_text[1])
			else:
				response_body = {'text': 'Ride Info Displayed'}
		# response_body = {'text': 'No End Point Can Satisfy This Request' }
	else:
		response_body = {'text': 'Internal Application Error'}

	# response_body = {'text': request.data}
	# response = jsonify(response_body)
	
	response = jsonify(response_body)
	response.status_code = 200
	return response

if __name__ == '__main__':
	manager.run()
