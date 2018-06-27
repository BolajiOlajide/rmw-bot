from .base import db, Base


class User(Base, db.Model):

	__tablename__ = 'users'
	__table_args__ = (db.UniqueConstraint(
        'slack_uid', 'slack_name', name='unique_constraint_user'),)

	slack_uid = db.Column(db.String(50), nullable=False)
	slack_name = db.Column(db.String(80), nullable=False)
	full_name = db.Column(db.String(100), nullable=False)
	phone_number = db.Column(db.String(20))

	def __init__(self, slack_uid, slack_name, full_name, phone_number):
		self.slack_uid = slack_uid
		self.slack_name = slack_name
		self.full_name = full_name
		self.phone_number = phone_number

	def __repr__(self):
		return "<User: Full Name: {} - Slack ID: {} - \
				Slack Name: {} and \
				Phone Number: {}>".format(
										  self.full_name, self.slack_uid,
										  self.slack_name, self.phone_number)
