from sqlalchemy import String , Integer
from db import db


class userModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    firstName = db.Column(String(80), nullable=False)
    lastName = db.Column(String(80), nullable=False)
    pwd = db.Column(String(80) , nullable=False)
    userName = db.Column(String(80) , nullable=False , unique=True)
    passengers = db.relationship('passengerModel', backref='users')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


