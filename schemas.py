from marshmallow import Schema, fields

class userCredSchema(Schema):
    userName = fields.String(required=True)
    pwd = fields.String(required=True)

class userPersonalInfoSchema(Schema):

    id = fields.Integer(required=True , dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    userName = fields.Str(required=True)
    pwd = fields.Str(required=True , load_only=True)


class passengerDetSchema(Schema):

    id = fields.Integer(required=True , dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    pnr = fields.Str()
    seatNum = fields.Str()
    amtPaid = fields.Integer()
    userId = fields.Integer()


class userPassengerSchema(userPersonalInfoSchema):

    passengerDetails = fields.List(fields.Nested(passengerDetSchema))


class flightDetSchema(Schema):

    id = fields.Integer(required=True , dump_only=True)
    pnr = fields.Str(required=True)
    origin = fields.Str(required=True)
    destination = fields.Str(required=True)
    flightTime = fields.DateTime("%Y-%m-%d" , required=True)
    basicFare = fields.Float(required=True)

class seatSchema(Schema):

    id = fields.Integer(required=True , dump_only=True)
    seatNum = fields.Str(required=True)
    seatPrice = fields.Float(required=True)
    seatType = fields.String(required=True)
    flightId = fields.Integer(required=True , dump_only=True)
    passengerId = fields.Integer()


class flightSeatSchema(flightDetSchema):

    seat_id = fields.Integer(required=True , dump_only=True)
    seats = fields.Nested(seatSchema , required=True)


