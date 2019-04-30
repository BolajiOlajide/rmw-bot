from datetime import datetime
from time import ctime

from app.repositories.ride_repo import RideRepo
from app.repositories.ride_rider_repo import RideRiderRepo
from app.repositories.user_repo import UserRepo
from app.utils import timestamp_to_epoch, convert_time_to_timestamp, slackhelper, check_ride_status


class BotActions:

	def __init__(self, current_user=None):
		self.ride_repo = RideRepo()
		self.user_repo = UserRepo()
		self.ride_rider_repo = RideRiderRepo()
		if current_user is not None:
			self.current_user = current_user

	def add_ride(self, origin, destination, take_off, max_seats):

		if take_off.find(':') < 1:
			error_msg = "The time format provided is invalid. It must be in 24hr format: 08:00 or 18:59"
			msg = {
				"errors": [
					{
						"name": "take_off",
						"error": error_msg
					}
				]
			}
			return msg

		try:
			max_seats = int(max_seats)
		except ValueError:
			max_seats = None

		if not isinstance(max_seats, int):
			msg = {
				"errors": [
					{
						"name": "max_seats",
						"error": "Number of riders must be integer (example: 2)"
					}
				]
			}
			return msg

		take_off_time = convert_time_to_timestamp(take_off)

		if self.ride_repo.is_ride_exist(self.current_user.id, origin, destination, take_off_time):
			msg_1 = ":no_entry_sign: Error occurred! Ride With Provided Details Already Exist. -"
			msg_2 = "`/rmw show-rides` to get all rides."
			msg = {"text": "{} {}".format(msg_1, msg_2)}
			return msg

		ride_args = {
			"driver_id": self.current_user.id,
			"origin": origin,
			"destination": destination,
			"take_off": take_off_time,
			"max_seats": max_seats,
			"seats_left": max_seats,
			"status": 1
		}

		new_ride_data = self.ride_repo.new_ride(**ride_args)

		if new_ride_data:
			destination=new_ride_data.destination
			origin=new_ride_data.origin
			take_off=ctime(new_ride_data.take_off.timestamp())
			max_seats=new_ride_data.max_seats
			text = f""">>>:white_check_mark: Ride to {destination}, from {origin}, by {take_off} saved!
Thanks for sharing {max_seats} spaces."""
			msg = {"text": text}
			return msg
		else:
			msg = {"text": ":no_entry_sign: Error occurred saving Ride! Please try again."}
			return msg

	def get_ride_info(self, _id):
		ride = self.ride_repo.find_by_id(_id)

		if not ride:
			return {'text': 'No Ride With Provided ID. - `/rmw show-rides` to get all rides.'}
		else:
			driver_detail = '{} - <@{}> - {}'.format(
				ride.driver.full_name, ride.driver.slack_uid, ride.driver.phone_number)

			# The extra curly braces inside the format() is specifically for slack formatting.
			# Please leave as-is
			takeoff_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(
				epoch=timestamp_to_epoch(ride.take_off),
				date='{date_short_pretty}',
				time='{time}', fallback=ride.take_off)

			ride_status = check_ride_status(ride)
			text = f"""
Details for Ride _{_id}_:
>>>*Driver Details:* _{driver_detail}_
*Origin:* _{ride.origin}_
*Destination:* _{ride.destination}_
*Take Off Time:* _{takeoff_time}_
*Seats Available:* _{ride.seats_left}_
*Status:* _{ride_status}_
"""

			# return {'text': 'Details for Ride {}: \n ```\n Driver Details: {}\
			# 				\n Origin: {}\n Destination: {} \n Take Off Time: {}\
			# 				\n Seats Available: {}\n Status: {}```'.format(
			# 	id, driver_detail, ride.origin, ride.destination, takeoff_time,
			# 	ride.seats_left, ride_status)}
			return {'text': text}

	def join_ride(self, id):
		ride = self.ride_repo.find_by_id(id)

		if not ride or ride.status == 0:
			return {'text': 'Ride Does Not Exists Or Is Expired. - `/rmw show-rides` to get all rides.'}
		else:
			if ride.seats_left < 1 or self.ride_rider_repo.count_ride_riders(ride.id) == ride.max_seats \
				or self.ride_rider_repo.is_rider_already_joined(
						ride_id=ride.id, rider_id=self.current_user.id):
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

		if len(rides) > 0:
			for ride in rides:
				# format the take_of_time string
				take_off_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(
					epoch=timestamp_to_epoch(ride.take_off), date='{date_short_pretty}', time='{time}',
					fallback=ride.take_off)
				ride_status = check_ride_status(ride)
				# text += str('```Ride Id: {} \nDriver name: {} <@{}> \n\
				# 			Driver number: {} \nSpace available: {} \nPick up point: {} \n\
				# 			Destination: {} \nTake off: {} \nStatus: {}```\n').format(
				# 	ride.id, ride.driver.full_name, ride.driver.slack_uid,
				# 	ride.driver.phone_number,
				# 	ride.seats_left, ride.origin, ride.destination, take_off_time,
				# 	ride_status)
				text += f"""```Ride Id: {ride.id}
Driver name: {ride.driver.full_name} <@{ride.driver.slack_uid}>
Driver number: {ride.driver.phone_number}
Space available: {ride.seats_left}
Pick up point: {ride.origin}
Destination: {ride.destination}
Take off: {take_off_time}
Status: {ride_status}```
"""
		else:
			text = ':disappointed: No rides available for now, please check back later in the day'

		return {
			'text': text,
		}

	def cancel_ride(self, id):
		ride = self.ride_repo.find_by_id(id)

		if self.current_user.id != ride.driver_id:
			return {'text': 'You are not authorized to cancel this ride'}

		if not ride:
			return {'text': 'Ride Does Not Exist'}
		ride_status = check_ride_status(ride)

		if ride_status == 'INACTIVE':
			return {'text': 'This Ride is currently expired or cancelled'}

		ride_riders = self.ride_rider_repo.ride_rider_list(ride.id)

		take_off_time = '<!date^{epoch}^{date} at {time}|{fallback}>'.format(
			epoch=timestamp_to_epoch(ride.take_off),
			date='{date_short_pretty}', time='{time}',
			fallback=ride.take_off)

		text = 'Sorry :disappointed: {} has cancelled the {} to {} ride for {}. \
			- Please check for other rides.' \
			.format(self.current_user.full_name, ride.origin, ride.destination, take_off_time)

		ride.status = 0

		ride.save()

		for ride_rider in ride_riders:
			rider = self.user_repo.find_by_id(ride_rider.rider_id)
			return slackhelper.post_message(text, rider.slack_uid)

		response_text = 'Your Ride has been cancelled successfully'

		return {
			'text': response_text
		}
