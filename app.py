from flask import send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db
from views.blog import blog_bp
from views.auth import auth_bp
from utils.app import create_app

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
