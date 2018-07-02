from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

allowed_commands = [
	'add-vehicle',
	'move-vehicle',
	'remove-vehicle',
	'who-is',
	'help'
]
