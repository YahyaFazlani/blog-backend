import os
from datetime import timedelta


class Config(object):
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = "./media/thumbnails"
  ALLOWED_EXTENSIONS = tuple({".jpeg", ".jpg", ".png", ".gif"})
  SECRET_KEY = os.environ.get("SECRET_KEY")
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(Config):
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
  SECRET_KEY = "fjdsajfksd"
