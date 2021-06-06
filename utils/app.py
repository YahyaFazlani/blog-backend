from flask import Flask


def create_app():
  UPLOAD_FOLDER = "./media/thumbnails"
  ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif"}

  app = Flask(__name__)
  app.secret_key = "kjsdkjjfhgukahyejfds"

  app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
  app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  return app
