from flask_limiter import Limiter
from flask.views import MethodView
from flask import request , jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from flask_smorest import abort , Blueprint
from flask_limiter.util import get_remote_address

from db import db
from datetime import datetime
from models import userModel , flightModel , seatModel
from schemas import flightSeatSchema , flightDetSchema , seatSchema

blp = Blueprint("flight" , __name__ , description='Operations on flights')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)


def findSeat(seatNum , flightId):
    flight = seat = None
    flight = flightModel.query.filter(flightModel.id == flightId).first()
    if flight:
        seats = flight.seats
        for seat_ in seats:
            if seat_.seatNum == seatNum and seat_.passengerId == None:
                seat = seat_
    return flight , seat
            
@blp.route('/api/flight/new-flight' , methods=['POST'])
@limiter.limit('5 per minute')
@blp.response(200 , flightDetSchema)
def newFlight():
    req_json = request.get_json()
    flight_time_str = req_json['flightTime']
    flight_time = datetime.strptime(flight_time_str, '%Y-%m-%d').date()
    req_json['flightTime'] = flight_time
    flight = flightModel(**req_json)

    try:
        db.session.add(flight)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return abort(500 , 'User info not registered')
    
    return flight


@blp.route('/api/flight/new-flight/seats' , methods=['POST'])
@limiter.limit('5 per minute')
@blp.response(200 , seatSchema)
def newSeats():
    req_json = request.get_json()

    try:
        seats = [seatModel(**data) for data in req_json]
        db.session.add_all(seats)
        db.session.commit()

    except SQLAlchemyError:
        return abort(500 , 'Failed to create seats')

    return jsonify([seat.to_dict() for seat in seats])



@blp.route('/api/flight/book/<int:flightId>' , methods=['PUT'])
class bookFlight(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.response(200 , flightSeatSchema)
    def put(self , flightId):
        userId = int(request.args.get('userId'))
        passengerId = int(request.args.get('passengerId'))
        seatNum = request.args.get('seatNum')
        
        user = userModel.query.filter(userModel.id == userId).first()
        flight , seat = findSeat(seatNum , flightId)

        if seat == None:
            return abort(401 , 'Booking Not Registered')
        
        if user:
            passengers = user.passengers
            for passenger in passengers:
                if passenger.id == passengerId:
                    seat.passengerId = passengerId
                    passenger.pnr = flight.pnr
                    passenger.amtPaid = flight.basicFare + seat.seatPrice
                    passenger.seatNum = seat.seatNum
                    try:
                        db.session.add(seat)
                        db.session.add(passenger)
                        db.session.commit()
                        return passenger.to_dict()
                    except Exception as e:
                        print(str(e))
                        return abort(500 , 'Booking Incomplete')                        
            return abort(401 , 'Passenger Not Found')
        else:
            abort(401, 'User Not Found')

