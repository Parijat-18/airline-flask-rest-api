from flask import request , jsonify
from flask.views import MethodView
from flask_limiter import Limiter
from models import userModel , passengerModel
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db
from flask_smorest import abort , Blueprint
from flask_limiter.util import get_remote_address
from schemas import passengerDetSchema


blp = Blueprint("passenger" , __name__ , description='User Info and Authentication')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)


@blp.route('/api/user/<int:userId>/passengers/edit')
class Passengers(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.arguments(passengerDetSchema , location='json' , as_kwargs=True)
    @blp.response(201 , passengerDetSchema)
    def put(self , userId , **req_json):

        passengerId = int(request.args.get('id'))
        user = userModel.query.get_or_404(userId)
        if user:
            passengers = user.passengers
            for passenger in passengers:
                if passenger.id == passengerId:
                    passenger.firstName = req_json['firstName']
                    passenger.lastName = req_json['lastName']
                    try:
                        db.session.add(passenger)
                        db.session.commit()
                        return jsonify(passenger.to_dict())
                    except SQLAlchemyError:
                        abort(402 , message='Passenger Registration Failed')
            return abort(401 , message='Passenger Not Found')
        else:
            abort(401 , message='User Not Found')

    @jwt_required()
    @limiter.limit('5 per minute')
    def delete(self , userId):
        passengerId = int(request.args.get('id'))
        user = userModel.query.get_or_404(userId)
        if user:
            passengers = user.passengers
            for passenger in passengers:
                if passenger.id == passengerId:
                    try:
                        db.session.delete(passenger)
                        db.session.commit()
                    except SQLAlchemyError:
                        abort(402 , message='Passenger Deletion Failed')
                    return jsonify({"message": "Passenger Deleted Successfully"})
            else:
                abort(401 , message='Passenger Not Found')
        else:
            abort(401 , message='User Not Found')

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.arguments(passengerDetSchema , location='json' , as_kwargs=True)
    @blp.response(201 , passengerDetSchema)
    def post(self , userId , **req_json):
        user = userModel.query.get_or_404(userId)
        req_json['userId'] = userId
        print(req_json)
        if user:
            passenger = passengerModel(**req_json)
            try:
                db.session.add(passenger)
                db.session.commit()
            except SQLAlchemyError:
                abort(500 , message='Passenger Registration Failed')
            return passenger
        else:
            abort(401 , message='User Not Found')



@blp.route('/api/user/<int:userId>/passengers' , methods=['GET'])
class passengerDetails(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.response(200 , passengerDetSchema)
    def get(self , userId):
        user = userModel.query.get_or_404(userId)
        if user:
            passengers = user.passengers
            if passengers:
                resp = [passenger.to_dict() for passenger in passengers]
                return jsonify(resp)
            else:
                {abort(401 , message="No Passengers")}
        else:
            abort(401 , message='User Not Found')