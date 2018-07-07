from app.repositories.ride_repo import RideRepo
from app.repositories.ride_rider_repo import RideRiderRepo
from app.utils import timestamp_to_epoch
from datetime import datetime


class BotActions:
	
	def __init__(self, current_user=None):
		self.ride_repo = RideRepo()
		self.ride_rider_repo = RideRiderRepo()
		if current_user is not None:
			self.current_user = current_user
	
	def get_ride_info(self, id):
		ride = self.ride_repo.find_by_id(id)
		
		if not ride:
			return {'text': 'No Ride With Provided ID. - `/rmw show-rides` to get all rides.'}
		else:
			driver_detail = '{} - <@{}> - {}'.format(ride.driver.full_name, ride.driver.slack_uid, ride.driver.phone_number)
			
			# The extra curly braces inside the format() is specifically for slack formating. Please leave as-is
			takeoff_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(epoch=timestamp_to_epoch(ride.take_off), date='{date_short_pretty}', time='{time}', fallback=ride.take_off)
			if ride.status == 0:
				ride_status = 'EXPIRED'
			else:
				ride_status = 'ACTIVE'
			
			return {'text': 'Details for Ride {}: \n'
							' ```\n Driver Details: {}'
							'\n Origin: {}'
							'\n Destination: {} '
							'\n Take Off Time: {}'
							'\n Seats Available: {}'
							'\n Status: {}```'.format(id, driver_detail, ride.origin, ride.destination, takeoff_time,
															ride.seats_left, ride_status)}
	
	def join_ride(self, id):
		ride = self.ride_repo.find_by_id(id)
		
		if not ride or ride.status == 0:
				return {'text': 'Ride Does Not Exists Or Is Expired. - `/rmw show-rides` to get all rides.'}
		else:
			if ride.seats_left < 1 or self.ride_rider_repo.count_ride_riders(ride.id) == ride.max_seats \
					or self.ride_rider_repo.is_rider_already_joined(ride_id=ride.id, rider_id=self.current_user.id):
				return {'text': 'Sorry, You\'re Already Booked or This Ride Is Fully Booked'}
			else:
				self.ride_rider_repo.new_ride_rider(ride_id=ride.id, rider_id=self.current_user.id)
				self.ride_repo.decrement_seats_left(ride)
				return {'text': 'Successfully Joined Ride'}

	def show_rides(self):
		todays_date = datetime.now()
		start = datetime(todays_date.year, todays_date.month, todays_date.day, 0, 0)
		end = datetime(todays_date.year, todays_date.month, todays_date.day, 23, 59)
		rides = RideRepo.get_todays_rides(start=start, end=end)

		text = ''

		for ride in rides:
			# format the take_of_time string
			take_off_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(epoch=timestamp_to_epoch(ride.take_off), date='{date_short_pretty}', time='{time}', fallback=ride.take_off)
			text += str('```Ride Id: {} \n'
				'Driver name: {} \n'
				'Driver number: {} \n'
				'Space available: {} \n'
				'Pick up point: {} \n'
				'Destination: {} \n'
				'Take off: {} \n```\n').format(ride.id, ride.driver.full_name, ride.driver.phone_number, 
			ride.seats_left, ride.origin, ride.destination, take_off_time)

		return {
			'text': text,
		}
					

