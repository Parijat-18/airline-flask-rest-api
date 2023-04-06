from sqlalchemy import String , Date , Float , Integer
from db import db


class flightModel(db.Model):
    __tablename__ = 'flights'

    id = db.Column(Integer, primary_key=True)
    pnr = db.Column(String(10), unique=True, nullable=False)
    origin = db.Column(String(4), nullable=False)
    destination = db.Column(String(4), nullable=False)
    flightTime = db.Column(Date , nullable=False)
    basicFare = db.Column(Float(precision=2), nullable=False)
    seats = db.relationship('seatModel', backref='flight')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class seatModel(db.Model):
    __tablename__ = 'seats'

    id = db.Column(Integer, primary_key=True)
    seatNum = db.Column(String(4), nullable=False, unique=True)
    seatPrice = db.Column(Float(precision=2), nullable=False, unique=False)
    seatType = db.Column(String(20) , nullable=False , default='economy')
    flightId = db.Column(Integer, db.ForeignKey('flights.id'), nullable=False)
    passengerId = db.Column(Integer , db.ForeignKey('passengers.id') , nullable=True)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}