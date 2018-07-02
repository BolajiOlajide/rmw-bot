from app.repositories.ride_repo import RideRepo
from app.utils import timestamp_to_epoch


class BotActions:
	
	def __init__(self):
		self.ride_repo = RideRepo()
    
    def add_ride():
        return 'i am adding ride'
	
	def get_ride_info(self, id):
		ride = self.ride_repo.find_by_id(id)
		
		if not ride:
			return {'text': 'No Ride With Provided ID. - `/rmw show-rides` to get all rides.'}
		else:
			driver_detail = '{} - <@{}> - {}'.format(ride.driver.full_name, ride.driver.slack_uid, ride.driver.phone_number)
			
			# The extra curly braces inside the format() is specifically for slack formating. Please leave as-is
			takeoff_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(epoch=timestamp_to_epoch(ride.take_off), date='{date_short_pretty}', time='{time}', fallback=ride.take_off)
			
			return {'text': 'Details for Ride {}: \n'
							' ```\n Driver Details: {}'
							'\n Origin: {}'
							'\n Destination: {} '
							'\n Take Off Time: {}'
							'\n Seats Available: {}```'.format(id, driver_detail, ride.origin, ride.destination, takeoff_time,
															ride.seats_left)}
