from app.utils import db
from datetime import datetime


class User(db.Model):
	
	__tablename__ = 'users'
	
	id = db.Column(db.Integer(), primary_key=True)
	slack_uid = db.Column(db.String(50), nullable=False)
	slack_name = db.Column(db.String(80), nullable=False)
	full_name = db.Column(db.String(100), nullable=False)
	phone_number = db.Column(db.String(20))
	created_at = db.Column(db.DateTime(), default=datetime.now())
	updated_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
	
	def __init__(self, slack_uid, slack_name, full_name, phone_number):
		self.slack_uid = slack_uid
		self.slack_name = slack_name
		self.full_name = full_name
		self.phone_number = phone_number
	
	def save(self):
		db.session.add(self)
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def __repr__(self):
		return "<User: Full Name: {} - Slack ID: {} - Slack Name: {} and Phone Number: {}>".format(self.full_name, self.slack_uid, self.slack_name, self.phone_number)


