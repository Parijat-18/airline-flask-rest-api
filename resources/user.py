from flask import request , jsonify
from flask.views import MethodView
from flask_limiter import Limiter
from models import userModel , BLOCKLIST
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort , Blueprint
from flask_limiter.util import get_remote_address
from flask_jwt_extended import create_access_token , jwt_required , create_refresh_token , get_jwt , get_jwt_identity

from db import db
from passlib.hash import pbkdf2_sha256
from schemas import userCredSchema , userPersonalInfoSchema

blp = Blueprint("user" , __name__ , description='User Authentication and Security')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)


@blp.route('/api/register')
class Register(MethodView):

    @limiter.limit('5 per minute')
    @blp.arguments(userPersonalInfoSchema)
    def post(self , req_json):
        if userModel.query.filter(userModel.userName == req_json['userName']).first():
            abort(409 , message='Username Already Exists')

        req_json['pwd'] = pbkdf2_sha256.hash(req_json['pwd'])
        user = userModel(**req_json)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(401 , message='User Registration Failed')

        return jsonify({"userName":user.userName , "pwd":user.pwd})
    


@blp.route('/api/login')
class Login(MethodView):

    @limiter.limit('5 per minute')
    @blp.arguments(userCredSchema)
    def post(self , req_json):

        user = userModel.query.filter(userModel.userName == req_json['userName']).first()

        if user and pbkdf2_sha256.verify(req_json['pwd'] , user.pwd):
            access_token = create_access_token(identity=user.id , fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token":access_token , "refresh_token":refresh_token}
        return abort(401 , 'Invalid Credentials')
    

@blp.route('/api/logout')
class Logout(MethodView):

    @jwt_required()
    @limiter.limit('5 per minute')
    def post(self):
        jti = get_jwt()['jti']
        new_jti = BLOCKLIST(**{'jti':jti})
        db.session.add(new_jti)
        db.session.commit()
        return {'message':"Successfully Logged Out"} , 200



@blp.route("/api/refresh")
class TokenRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
