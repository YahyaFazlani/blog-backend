from flask_restful import reqparse
from utils.validate import validate_email

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument("firstname", type=str, required=True)
user_register_parser.add_argument("lastname", type=str, required=True)
user_register_parser.add_argument("email", type=validate_email, required=True)
user_register_parser.add_argument("password", type=str, required=True)

user_login_parser = user_register_parser.copy()
user_login_parser.remove_argument("firstname")
user_login_parser.remove_argument("lastname")