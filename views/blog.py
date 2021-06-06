from flask import Blueprint, url_for
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Api, Resource, abort, fields, marshal_with
from models import Blog as BlogModel
from models import User as UserModel
from models import db
from werkzeug.datastructures import FileStorage
from utils.parsers.blog_parsers import blog_create_parser, blog_update_parser
from utils.file import create_filename, get_extension, is_allowed

blog_bp = Blueprint("blogs", __name__)
api = Api(blog_bp)

blog_resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "thumbnail": fields.Url,
    "author": fields.Integer,
    "is_published": fields.Boolean,
}


class Blogs(Resource):
  @marshal_with(blog_resource_fields)
  def get(self):
    blogs = BlogModel.query.all()

    return blogs

  @marshal_with(blog_resource_fields)
  @jwt_required()
  def post(self):
    args = blog_create_parser.parse_args()

    author_email = get_jwt_identity()
    author: UserModel = UserModel.query.filter_by(email=author_email).first()

    is_published = args["is_published"] if "is_published" in args else False
    thumbnail: FileStorage = args["thumbnail"]

    if is_allowed(thumbnail.name):
      extension = get_extension(thumbnail.name)
      filename = create_filename(author.id, args["title"], extension)
      filepath = f"media/thumbnails/{filename}"
      thumbnail.save(filepath)

      thumbnail_url = url_for("media", path=filepath, _external=True)

      blog = BlogModel(
          title=args["title"], content=args["content"], author=author.id, thumbnail=thumbnail_url, is_published=is_published)

      db.session.add(blog)
      db.session.commit()

      return blog, 201

    abort(400, message="File is not an image file")


class Blog(Resource):
  @staticmethod
  def blog_exists_quit(blog_id: int):
    blog_exists = BlogModel.query.get(blog_id)

    if blog_exists:
      abort(409, message="blog already exists")

    del blog_exists

  @marshal_with(blog_resource_fields)
  @jwt_required(optional=True)
  def get(self, blog_id):
    blog = BlogModel.query.get(blog_id)
    author_email = get_jwt_identity()

    if author_email is None and blog.is_published == False:
      abort(404)

    author = UserModel.query.filter_by(email=author_email).first()

    if blog.is_published == False and blog.author != author.id:
      abort(404)

    return blog

  @marshal_with(blog_resource_fields)
  @jwt_required()
  def put(self, blog_id):
    self.blog_exists_quit(blog_id)

    args = blog_create_parser.parse_args()
    author_email = get_jwt_identity()
    author = UserModel.query.filter_by(dict(email=author_email)).first()

    is_published = args["is_published"] if "is_published" in args else False

    blog = BlogModel(
        title=args["title"], content=args["content"], author=author.id, is_published=is_published)

    db.session.add(blog)
    db.session.commit()

    return blog, 201

  @marshal_with(blog_resource_fields)
  def patch(self, blog_id):
    self.blog_exists_quit(blog_id)

    args = blog_update_parser.parse_args()

    blog: BlogModel = BlogModel.query.get(blog_id)

    blog.title = args["title"] if "title" in args else blog.title
    blog.content = args["content"] if "content" in args else blog.content
    blog.is_published = args["is_published"] if "is_published" in args else blog.is_published

    db.session.commit()

    return blog, 200

  # @jwt_required
  def delete(self, blog_id):
    blog: BlogModel = BlogModel.query.get(blog_id)

    if not blog:
      abort(404, message="blog does not exist")

    print(blog.author)

    db.session.delete(blog)
    db.session.commit()

    return {"message": "blog successfully deleted"}, 200


api.add_resource(Blogs, "/")
api.add_resource(Blog, "/<int:blog_id>")
