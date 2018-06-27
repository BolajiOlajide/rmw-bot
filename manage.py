from flask_script import Manager
from flask import jsonify
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.utils import db
from config import get_env

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['POST', 'GET'])
def home():
    response_body = {
        'status': 'success',
        'msg': 'You Are Ready To Ride My Way'
    }
    response = jsonify(response_body)
    response.status_code = 200
    return response


if __name__ == '__main__':
    manager.run()
