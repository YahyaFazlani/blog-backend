from flask_restful import reqparse

blog_create_parser = reqparse.RequestParser()
blog_create_parser.add_argument("title", type=str, required=True)
blog_create_parser.add_argument("content", type=str, required=True)
# blog_create_parser.add_argument("author", type=int, required=True)
blog_create_parser.add_argument("is_published", type=bool, required=False)

blog_update_parser = reqparse.RequestParser()
blog_update_parser.add_argument("title", type=str, required=False)
blog_update_parser.add_argument("content", type=str, required=False)
blog_update_parser.add_argument("author", type=int, required=False)
blog_update_parser.add_argument("is_published", type=bool, required=False)
