class Config(object):
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = "./media/thumbnails"
  ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif"}
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"


class DevelopmentConfig(Config):
  pass


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
