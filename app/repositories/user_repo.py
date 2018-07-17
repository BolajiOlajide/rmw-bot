from app.models.user import User


class UserRepo:
	
	@staticmethod
	def find_by_id(id):
		return User.query.filter_by(id=id).first()
	
	@staticmethod
	def find_by_slackid(slack_id):
		return User.query.filter_by(slack_uid=slack_id).first()
	
	@staticmethod
	def all():
		return User.query.all()
	
	@staticmethod
	def new_user(slack_uid, slack_name, full_name, phone_number):
		user = User(slack_uid=slack_uid, slack_name=slack_name, full_name=full_name, phone_number=phone_number)
		user.save()
		return user

