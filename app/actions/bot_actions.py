from datetime import datetime
from time import ctime

from app.repositories.ride_repo import RideRepo
from app.repositories.ride_rider_repo import RideRiderRepo
from app.repositories.user_repo import UserRepo
from app.utils import (check_ride_status, convert_time_to_timestamp,
                       slackhelper, timestamp_to_epoch)


class BotActions:
    def __init__(self, current_user=None):
        self.ride_repo = RideRepo()
        self.user_repo = UserRepo()
        self.ride_rider_repo = RideRiderRepo()
        if current_user is not None:
            self.current_user = current_user

    def add_ride(self, origin, destination, take_off, max_seats):

        if take_off.find(":") < 1:
            error_msg = "The time format provided is invalid. It must be in 24hr format: 08:00 or 18:59"
            msg = {"errors": [{"name": "take_off", "error": error_msg}]}
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
                        "error": "Number of riders must be integer (example: 2)",
                    }
                ]
            }
            return msg

        take_off_time = convert_time_to_timestamp(take_off)

        if self.ride_repo.is_ride_exist(
            self.current_user.id, origin, destination, take_off_time
        ):
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
            "status": 1,
        }

        new_ride_data = self.ride_repo.new_ride(**ride_args)

        if new_ride_data:
            destination = new_ride_data.destination
            origin = new_ride_data.origin
            take_off = ctime(new_ride_data.take_off.timestamp())
            max_seats = new_ride_data.max_seats
            text = f""">>>:white_check_mark: Ride to {destination}, from {origin}, by {take_off} saved!
Thanks for sharing {max_seats} spaces."""
            msg = {"text": text}
            return msg
        else:
            msg = {
                "text": ":no_entry_sign: Error occurred saving Ride! Please try again."
            }
            return msg

    def get_ride_info(self, _id):
        ride = self.ride_repo.find_by_id(_id)

        if not ride:
            return {
                "text": "No Ride With Provided ID. - `/rmw show-rides` to get all rides."
            }
        else:
            driver_detail = "{} - <@{}> - {}".format(
                ride.driver.full_name, ride.driver.slack_uid, ride.driver.phone_number
            )

            # The extra curly braces inside the format() is specifically for slack formatting.
            # Please leave as-is
            takeoff_time = "<!date^{epoch}^{date} at {time}|{fallback}>".format(
                epoch=timestamp_to_epoch(ride.take_off),
                date="{date_short_pretty}",
                time="{time}",
                fallback=ride.take_off,
            )

            ride_status = check_ride_status(ride)
            rider_count = self.ride_rider_repo.count_ride_riders(_id)
            seats_left = ride.max_seats - rider_count
            text = f"""
Details for Ride ID: _{_id}_:
>>>*Driver Details:* _{driver_detail}_
*Origin:* _{ride.origin}_
*Destination:* _{ride.destination}_
*Take Off Time:* _{takeoff_time}_
*Seats Available:* _{seats_left}_
*Status:* _{ride_status}_
"""
            return {"text": text}

    def join_ride(self, _id):
        ride = self.ride_repo.find_by_id(_id)
        rider_count = self.ride_rider_repo.count_ride_riders(ride.id)
        seats_left = ride.max_seats - rider_count

        if not ride or ride.status == 0:
            return {
                "text": "Ride Does Not Exists Or Has Expired. - `/rmw show-rides` to get all rides."
            }
        else:
            if ride.driver.id == self.current_user.id:
                return {
                    "text": ">Sorry, You can't be a driver and a rider at the same time. Calm down! :chop-slap: "
                }
            elif seats_left < 1 or rider_count == ride.max_seats:
                return {"text": "Sorry, This ride is full. Kindly join another ride."}
            elif self.ride_rider_repo.is_rider_already_joined(
                ride_id=ride.id, rider_id=self.current_user.id
            ):
                return {
                    "text": "Sorry, You're already booked for this ride. Don't stress me plix!"
                }
            else:
                self.ride_rider_repo.new_ride_rider(
                    ride_id=ride.id, rider_id=self.current_user.id
                )
                response_text = f""">>>Hey,
<@{self.current_user.slack_uid}> just joined your ride. :celebrate:"""
                slackhelper.post_message(response_text, ride.driver.slack_uid)
                return {
                    "text": f""">>>Hey <@{self.current_user.slack_uid}>,
You've successfully joined ride {ride.id}."""
                }

    def show_rides(self):
        todays_date = datetime.now()
        start = datetime(todays_date.year, todays_date.month, todays_date.day, 0, 0)
        end = datetime(todays_date.year, todays_date.month, todays_date.day, 23, 59)
        rides = RideRepo.get_todays_rides(start=start, end=end, status=1)

        text = "\n"

        if len(rides) > 0:
            for ride in rides:
                rider_count = self.ride_rider_repo.count_ride_riders(ride.id)
                seats_left = ride.max_seats - rider_count
                # format the take_off_time string
                take_off_time = "<!date^{epoch}^{date} at {time}|{fallback}>".format(
                    epoch=timestamp_to_epoch(ride.take_off),
                    date="{date_short_pretty}",
                    time="{time}",
                    fallback=ride.take_off,
                )
                ride_status = check_ride_status(ride)
                text += f""">*Ride Id*: {ride.id}
>_Driver name:_ <@{ride.driver.slack_uid}>
>_Pick up point:_ *{ride.origin}*
>_Destination:_ *{ride.destination}*
>_Status:_ *{ride_status}*

"""
        else:
            text = ":disappointed: No rides available for now, please check back later in the day"

        return {"text": text}

    def cancel_ride(self, _id):
        ride = self.ride_repo.find_by_id(_id)

        if self.current_user.id != ride.driver_id:
            return {
                "text": ">Why do you want to cancel what you didn't create. Why you gotta do like that :eyes:"
            }

        if not ride:
            return {"text": "Ride Does Not Exist"}
        ride_status = check_ride_status(ride)

        if ride_status == "INACTIVE":
            return {"text": "This Ride is currently expired or has been cancelled"}

        ride_riders = self.ride_rider_repo.ride_rider_list(ride.id)

        take_off_time = "<!date^{epoch}^{date} at {time}|{fallback}>".format(
            epoch=timestamp_to_epoch(ride.take_off),
            date="{date_short_pretty}",
            time="{time}",
            fallback=ride.take_off,
        )

        text = f"""Sorry 😞 <@{ride.driver.slack_uid}> has cancelled the {ride.origin} to {ride.destination} for {take_off_time}
Kindly opt-in for another ride.
"""
        ride.status = 0

        ride.save()

        for ride_rider in ride_riders:
            rider = self.user_repo.find_by_id(ride_rider.rider_id)
            slackhelper.post_message(text, rider.slack_uid)

        response_text = "Your Ride has been cancelled successfully."

        return {"text": response_text}

    def leave_ride(self, ride_id):
        ride_rider = self.ride_rider_repo.find_ride_rider(ride_id, self.current_user.id)
        text = (
            "🤨 You can't leave this ride as you are not an active rider on this ride."
        )
        if not ride_rider:
            return {"text": text}

        # set active status to false
        ride_rider.isActive = False
        ride_rider.save()

        response_text = f""">>>Hello,
<@{self.current_user.slack_uid}> has opted out of your ride thus opening up a space
for one more person.
"""
        driver_slack_id = ride_rider.ride.driver.slack_uid

        # notify driver
        slackhelper.post_message(response_text, driver_slack_id)

        return {
            "text": f"You've successful opted out of ride {ride_id} with <@{driver_slack_id}>"
        }
