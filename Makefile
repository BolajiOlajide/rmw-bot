APP_NAME=rmw

# Save dependencies
freeze:
	pip freeze > requirements.txt

migrate:
	python manage.py db migrate

upgrade:
	python manage.py db upgrade

# Start the application
start_dev:
	export FLASK_ENV=development && python manage.py runserver

# this command is for production purpose, it's why I used gunicorn here
start:
	gunicorn -w 6 -b 0.0.0.0 manage:app

install:
	pip intall -r requirements.txt
