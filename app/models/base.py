from datetime import datetime

from app.utils import db


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(
        db.DateTime(), default=datetime.now(), onupdate=datetime.now()
    )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except (exec.IntegrityError, exec.InvalidRequestError):
            db.session().rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
