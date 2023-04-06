from sqlalchemy import String , Integer , Float
from db import db


class passengerModel(db.Model):
    __tablename__ = 'passengers'

    id = db.Column(Integer, primary_key=True)
    firstName = db.Column(String(80), nullable=False)
    lastName = db.Column(String(80), nullable=False)
    seatNum = db.Column(String(4), nullable=True)
    amtPaid = db.Column(Float(precision=2), nullable=True)
    pnr = db.Column(String(10), nullable=True)
    userId = db.Column(Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    seat = db.relationship('seatModel' , backref='passengers' , uselist=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}