from .base import Base, db


class RideRider(Base, db.Model):
	__tablename__ = 'ride_riders'

	ride_id = db.Column(db.Integer(), db.ForeignKey('rides.id'))
	rider_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
	isActive = db.Column(db.Boolean(), default=True)

	ride = db.relationship("Ride")
	rider = db.relationship("User")

	def __init__(self, ride_id, rider_id):
		self.ride_id = ride_id
		self.rider_id = rider_id
