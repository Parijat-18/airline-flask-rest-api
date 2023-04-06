from flask import Flask , request , jsonify
from flask.views import MethodView
from flask_limiter import Limiter
from models import userModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
from passlib.hash import pbkdf2_sha256
from flask_smorest import abort , Blueprint
from flask_jwt_extended import jwt_required
from flask_limiter.util import get_remote_address
from schemas import userPersonalInfoSchema , userCredSchema , passengerDetSchema

blp = Blueprint("userinfo" , __name__ , description='User Info and Authentication')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)


    
@blp.route('/api/user/<int:userId>/user-info' , methods=['GET'])
class userInfoRetrieve(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.response(200 , userPersonalInfoSchema)
    def get(self , userId):
        user = userModel.query.filter(userModel.id == userId).first()
        if user:
            return jsonify(user.to_dict())
        else:
            return abort(401 , message='User Not Found')
    


@blp.route('/api/user/<int:userId>/user-info/edit')

class editUserInfo(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    @blp.response(200 , userPersonalInfoSchema)
    def put(self , userId):
        req_json = request.get_json()
        user = userModel.query.get_or_404(userId)
        if user:
            user.firstName = req_json['firstName']
            user.lastname = req_json['lastName']
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                abort(401 , message='User Info Update Failed')

            return jsonify(user.to_dict())
        else:
            return abort(401 , message='User Not Found')











