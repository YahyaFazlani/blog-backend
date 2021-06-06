from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db
from views.auth import auth_bp
from views.blog import blog_bp


def create_app(db_uri: str = "sqlite:///database.db"):
  UPLOAD_FOLDER = "./media/thumbnails"
  ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "gif"}

  app = Flask(__name__)

  app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
  app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
  app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  return app


app = create_app()


db.init_app(app)

CORS(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.errorhandler(IntegrityError)
def title_not_unique():
  return {"message": "title not unique"}, 400


@app.route("/media/<path:path>")
def media(path):
  return send_from_directory("media", path)


app.register_blueprint(blog_bp, url_prefix="/blog")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
  app.run(debug=True)
