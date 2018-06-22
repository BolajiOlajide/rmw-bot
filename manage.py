from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.utils import db
from config import get_env
from app.models import user

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
	manager.run()
