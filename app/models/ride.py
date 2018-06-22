from app.utils import db
from datetime import datetime


class Ride(db.Model):
	
	__tablename__ = 'rides'
	
	id = db.Column(db.Integer(), primary_key=True)
	driver_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
	origin = db.Column(db.String(100), nullable=False)
	destination = db.Column(db.String(80), nullable=False)
	take_off = db.Column(db.DateTime(), nullable=False)
	max_seats = db.Column(db.Integer(), nullable=False)
	seats_left = db.Column(db.Integer())
	status = db.Column(db.Integer())
	created_at = db.Column(db.DateTime(), default=datetime.now())
	updated_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
	
	def __init__(self, driver_id, origin, destination, take_off, max_seats=1, seats_left=1, status=1):
		self.driver_id = driver_id
		self.origin = origin
		self.destination = destination
		self.take_off = take_off
		self.max_seats = max_seats
		
		if max_seats > 1:
			seats_left = max_seats
		
		self.seats_left = seats_left
		self.status = status
	
	def save(self):
		db.session.add(self)
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def __repr__(self):
		return "<Ride Detail: Driver ID: {} - Origin: {} - Destination: {} - Take Off Time: {} - Seats Available: {}>".format(self.driver_id, self.origin, self.destination, self.take_off, self.seats_left)
	
	