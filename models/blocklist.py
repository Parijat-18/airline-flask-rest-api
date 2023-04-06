from db import db
from sqlalchemy import String , Integer


class BLOCKLIST(db.Model):
    __tablename__ = 'blocklist'
    id = db.Column(Integer , primary_key=True)
    jti = db.Column(String(80) , unique=True)