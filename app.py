from flask import Flask
from flask_cors import CORS

from models import db, migrate
from views.auth import auth_bp, jwt
from views.blog import blog_bp
from views.errorhandlers import error_bp
from views.media import media


def create_app(config="configs.DevelopmentConfig"):
  app = Flask(__name__)
  app.config.from_object(config)

  app.add_url_rule("/media/<path:path>", view_func=media)

  db.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app)
  CORS(app)

  app.register_blueprint(blog_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(error_bp)

  return app
