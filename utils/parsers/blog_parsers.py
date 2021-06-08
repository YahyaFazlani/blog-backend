from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

blog_create_parser = reqparse.RequestParser(bundle_errors=True)
blog_create_parser.add_argument("title", type=str, required=True)
blog_create_parser.add_argument("content", type=str, required=True)
blog_create_parser.add_argument(
    "thumbnail", type=FileStorage, location="files", required=True)
blog_create_parser.add_argument("is_published", type=bool, required=False)

blog_update_parser = blog_create_parser.copy()
blog_update_parser.replace_argument("title", required=False)
blog_update_parser.replace_argument("content", required=False)
blog_create_parser.replace_argument("thumbail", required=False)
blog_update_parser.replace_argument("is_published", required=False)
