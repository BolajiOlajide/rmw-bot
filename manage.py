from flask_script import Manager
from flask import request, jsonify
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.utils import db
from config import get_env

from app.controllers.ride import Ride

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


allowed_commands = [
    'add-ride'
    'add-rides'
]

@app.route('/', methods=['POST', 'GET'])
def home():
    response_body = {
        'status': 'success',
        'msg': 'You Are Ready To Ride My Way'
    }
    response = jsonify(response_body)
    response.status_code = 200
    return response

@app.route('/rides', methods=['POST'])
def rides():
    command_text = request.data.get('text')
    command_text = command_text.split(' ')
    slack_uid = request.data.get('user_id')
    ride_action = Ride()

    if command_text[0] not in allowed_commands:
        response_body = {'msg': 'Invalid Command Sent - `/rmw help` for available commands'}
    
    if command_text[0] in ['add-ride', 'add-rides']:
        response_body = response_body = {
            'status': 'success',
            'msg': ride_action.add_ride()
        }

    response = jsonify(response_body)
    response.status_code  = 200
    return response

if __name__ == '__main__':
    manager.run()
