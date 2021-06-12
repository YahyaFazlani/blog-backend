from flask import Blueprint
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt,
                                get_jwt_identity)
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Api, Resource, abort, fields
from models import db
from models.user import User as UserModel
from passlib.hash import pbkdf2_sha256 as sha256
from utils.parsers.user_parsers import user_register_parser, user_login_parser

jwt = JWTManager()
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(auth_bp)


@api.resource("/register")
class UserRegister(Resource):
  def post(self):
    args = user_register_parser.parse_args()

    user = UserModel.query.filter_by(email=args["email"]).first()

    if user:
      abort(
          409, message=f"user with the email '{args['email']}' already exists")

    del user

    new_user = UserModel(
        firstname=args["firstname"], lastname=args["lastname"], email=args["email"], password=sha256.hash(args["password"]))
    access_token = create_access_token(identity=args["email"], fresh=True)
    refresh_token = create_refresh_token(identity=args["email"])

    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "user was created",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@api.resource("/login")
class UserLogin(Resource):
  def post(self):
    args = user_login_parser.parse_args()
    user: UserModel = UserModel.query.filter_by(
        email=args["email"]).first()

    if not user:
      abort(404, message="user doesn't exist")

    if sha256.verify(args["password"], user.password):

      access_token = create_access_token(identity=args["email"], fresh=True)
      refresh_token = create_refresh_token(identity=args["email"])

      headers = [("Set-Cookie", f"access_token={access_token}; HttpOnly=true"), (
          "Set-Cookie", f"refresh_token={refresh_token}; HttpOnly=true")]

      return {
          "message": f"logged in as {user.email}",
          "access_token": access_token,
          "refresh_token": refresh_token
      }, 200, headers

    abort(401, message="invalid credentials")


@api.resource("/refresh")
class TokenRefresh(Resource):
  @jwt_required(refresh=True)
  def post(self):
    user = get_jwt_identity()
    access_token = create_access_token(identity=user, fresh=False)
    return {"access_token": access_token}, 200
