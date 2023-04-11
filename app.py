from flask_smorest import Api 
from flask import Flask , jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from models import BLOCKLIST
from resources.user import blp as UserBluePrint
from resources.flight import blp as flightBluePrint
from resources.userinfo import blp as UserInfoBluePrint
from resources.passenger import blp as PassengerBluePrint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config["API_TITLE"] = "Airline REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['JWT_SECRET_KEY'] = "6054879357072658146" # Better to save it as a SYS variable

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    migrate = Migrate(app  , db)

    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return BLOCKLIST.query.filter(BLOCKLIST.jti == jwt_payload["jti"]).one_or_none()


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token is not fresh.", "error": "fresh_token_required"}
            ),
            401,
        )


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(flightBluePrint)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(UserInfoBluePrint)
    api.register_blueprint(PassengerBluePrint)

    return app

create_app().run()