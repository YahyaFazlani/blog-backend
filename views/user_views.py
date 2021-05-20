from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Api, Resource, abort, fields
from models import User as UserModel, db
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import timedelta

from .parsers.user_parsers import user_create_parser

user_bp = Blueprint("users", __name__)
api = Api(user_bp)

user_resource_fields = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "email": fields.String,
    "password": fields.String,
    "is_author": fields.Boolean
}


class UserRegister(Resource):
  def post(self):
    args = user_create_parser.parse_args()

    user = UserModel.query.filter_by(email=args["email"]).first()
    print(user)

    if user:
      abort(
          409, message=f"user with the email '{args['email']}' already exists")

    del user

    new_user = UserModel(
        firstname=args["firstname"], lastname=args["lastname"], email=args["email"], password=sha256.hash(args["password"]))
    access_token = create_access_token(identity=args["email"])
    refresh_token = create_refresh_token(identity=args["email"])

    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "user was created",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


class UserLogin(Resource):
  def post(self):
    args = user_create_parser.parse_args()
    user: UserModel = UserModel.query.filter_by(
        email=args["email"]).first()

    if not user:
      abort(404, message="user doesn't exist")

    if sha256.verify(args["password"], user.password):

      access_token = create_access_token(identity=args["email"])
      refresh_token = create_refresh_token(identity=args["email"])

      headers = [("Set-Cookie", f"access_token={access_token}; HttpOnly=true"), (
          "Set-Cookie", f"refresh_token={refresh_token}; HttpOnly=true")]

      return {
          "message": f"logged in as {user.email}",
          "access_token": access_token,
          "refresh_token": refresh_token
      }, 200, headers

    abort(400, message="wrong credentials")


class TokenRefresh(Resource):
  @jwt_required(refresh=True)
  def post(self):
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    return {"access_token": access_token}


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
