from flask_script import Manager
from flask import jsonify, request
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.utils import db
from config import get_env

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/bot', methods=['POST', 'GET'])
def bot():
	command_text = request.data.get('text').split(" ")
	response_body = {'text': 'I do not understand that command. `/dash help` for available commands'}
	
	if command_text[0] not in allowed_commands:
		return jsonify({
			'text': str(guess_response('invalid_command')).format('sample')
		})
	
	response_body = {
		'status': 'success',
		'msg': 'You Are Ready To Ride My Way'
	}
	response = jsonify(response_body)
	response.status_code = 200
	return response


if __name__ == '__main__':
	manager.run()
