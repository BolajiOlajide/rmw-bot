from app.repositories.ride_repo import RideRepo
from app.utils import timestamp_to_epoch


class BotActions:
	
	def __init__(self):
		self.ride_repo = RideRepo()

	def add_ride(self, driver_id, origin, destination, take_off, max_seats):
		print('---i am ride repo action driver_id', driver_id)
		print("===>origin add===>", origin)
		print("===>destination add===>", destination)
		print("===>take_off add===>", take_off)
		print("===>max_seats add===>", int(max_seats))
		# new_ride = self.ride_repo.new_ride(driver_id=driver_id, origin=origin, destination=destination, take_off=take_off, max_seats=int(max_seats), seats_left=int(max_seats), status=1)
		# print('==>new ride saved in db:==>', new_ride)
		# msg = {"text": ":white_check_mark: Ride {ride_id} saved! Thanks for sharing.".format(ride_id=new_ride.driver_id)}
		msg = {"text": ":white_check_mark: Ride saved! Thanks for sharing."}

		return msg
	
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
