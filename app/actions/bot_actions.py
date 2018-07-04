from app.repositories.ride_repo import RideRepo
from app.utils import timestamp_to_epoch


class BotActions:
	
	def __init__(self):
		self.ride_repo = RideRepo()
		self.ride_details = {}

	def add_ride(self, driver_id, message_action_type):
		# get driver_id
		# generate callback_id = driver_id + 'add_ride'

		# if message_action_type == "interactive_message":
			# start dialogue
			# request for origin
			# on completion, request for destination
			# on completion, request for take_off [takeoff-time]
			# on completion, request for max_seats [space-available]
			# on completion, update for seats_left, with max_seats value then update status to 1
			# store in self.ride_detail hash

		# elif message_action_type == "dialog_submission":
			# new_ride = self.ride_repo.new_ride(self.ride_details.driver_id, self.ride_details.origin, self.ride_details.destination, self.ride_details.take_off, self.ride_details.max_seats, self.ride_details.max_seats, status)
		# return new_ride

		return {
			'text': 'New Ride Created Successfully - {}'.format(driver_id)
		}
	
	def get_ride_info(self, id):
		ride = self.ride_repo.find_by_id(id)
		
		if not ride:
			return {'text': 'No Ride With Provided ID. - `/rmw show-rides` to get all rides.'}
		else:
			driver_detail = '{} - <@{}> - {}'.format(ride.driver.full_name, ride.driver.slack_uid, ride.driver.phone_number)
			
			# The extra curly braces inside the format() is specifically for slack formatting. Please leave as-is
			takeoff_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(epoch=timestamp_to_epoch(ride.take_off), date='{date_short_pretty}', time='{time}', fallback=ride.take_off)
			
			return {'text': 'Details for Ride {}: \n'
							' ```\n Driver Details: {}'
							'\n Origin: {}'
							'\n Destination: {} '
							'\n Take Off Time: {}'
							'\n Seats Available: {}```'.format(id, driver_detail, ride.origin, ride.destination, takeoff_time,
															ride.seats_left)}
