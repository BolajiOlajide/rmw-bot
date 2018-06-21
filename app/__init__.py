from flask_api import FlaskAPI
from config.env import app_env
from app.utils import db
from flask import jsonify, request
import json


def create_app(config_name):
	app = FlaskAPI(__name__, instance_relative_config=False)
	app.config.from_object(app_env[config_name])
	app.config.from_pyfile('../config/env.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	
	@app.route('/', methods=['POST', 'GET'])
	def home():
		response_body = {'status': 'success', 'msg': 'You Are Ready To Ride My Way'}
		response = jsonify(response_body)
		response.status_code = 200
		return response
	
	return app
