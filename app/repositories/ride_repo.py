from app.models.ride import Ride


class RideRepo:
	
	@staticmethod
	def find_by_id(id):
		return Ride.query.filter_by(id=id).first()
	
	@staticmethod
	def all():
		return Ride.query.all()
	
	@staticmethod
	def increment_seats_left(ride):
		ride.seats_left += 1
		ride.save()

	@staticmethod
	def decrement_seats_left(ride):
		ride.seats_left -= 1
		ride.save()
	
	@staticmethod
	def new_ride(driver_id, origin, destination, take_off, max_seats=1, seats_left=1, status=1):
		ride = Ride(driver_id, origin, destination, take_off, max_seats, seats_left, status)
		ride.save()
		return ride

	@staticmethod
	def get_todays_rides(start=None, end=None):
		return Ride.query.filter(Ride.take_off <= end, Ride.take_off >= start).all()
