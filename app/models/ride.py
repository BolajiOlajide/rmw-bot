from .base import Base, db


class Ride(Base, db.Model):

    __tablename__ = "rides"

    driver_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    take_off = db.Column(db.DateTime(), nullable=False)
    max_seats = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.Integer())
    driver = db.relationship("User")

    def __init__(self, driver_id, origin, destination, take_off, max_seats=1, status=1):
        self.driver_id = driver_id
        self.origin = origin
        self.destination = destination
        self.take_off = take_off
        self.max_seats = max_seats
        self.status = status

    def __repr__(self):
        return "Ride Detail: Driver Name: {} | Origin: {} | Destination: {} | Take Off Time: {} | \
			Seats Available: {}".format(
            self.driver.full_name, self.origin, self.destination, self.take_off
        )
