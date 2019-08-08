from app.models.ride_rider import RideRider


class RideRiderRepo:
    @staticmethod
    def find_by_id(id):
        return RideRider.query.filter_by(id=id).first()

    @staticmethod
    def find_by_ride_id(ride_id):
        return RideRider.query.filter_by(ride_id=ride_id).first()

    @staticmethod
    def find_by_rider_id(rider_id):
        return RideRider.query.filter_by(rider_id=rider_id).first()

    @staticmethod
    def count_ride_riders(ride_id):
        return RideRider.query.filter_by(ride_id=ride_id, isActive=True).count()

    @staticmethod
    def is_rider_already_joined(ride_id, rider_id):
        query = RideRider.query.filter_by(
            ride_id=ride_id, rider_id=rider_id, isActive=True
        )
        if query.first():
            return True
        else:
            return False

    @staticmethod
    def ride_rider_list(ride_id):
        return RideRider.query.filter_by(ride_id=ride_id, isActive=True).all()

    @staticmethod
    def all():
        return RideRider.query.all()

    @staticmethod
    def new_ride_rider(ride_id, rider_id):
        ride_rider = RideRider(ride_id, rider_id)
        ride_rider.save()
        return ride_rider

    @staticmethod
    def find_ride_rider(ride_id, rider_id):
        return RideRider.query.filter_by(
            rider_id=rider_id, ride_id=ride_id, isActive=True
        ).first()

    @staticmethod
    def remove_ride_rider(ride_id, rider_id):
        ride_rider = RideRiderRepo.find_ride_rider(ride_id, rider_id).first()
        ride_rider.isActive = False
        ride_rider.save()
        return ride_rider
