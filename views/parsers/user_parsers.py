from flask_restful import reqparse

user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument("firstname", type=str, required=True)
user_create_parser.add_argument("lastname", type=str, required=True)
user_create_parser.add_argument("email", type=str, required=True)
user_create_parser.add_argument("password", type=str, required=True)
