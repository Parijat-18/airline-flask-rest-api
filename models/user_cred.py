from db import db
from sqlalchemy import String , Integer


class userCredModel(db.Model):
    __tablename__ = 'usercred'

    id = db.Column(Integer , primary_key=True)
    userName = db.Column(String , nullable=False , unique=True)
    pwd = db.Column(String , nullable=False)