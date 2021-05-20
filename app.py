from flask import Flask
from flask_migrate import Migrate
from flask_restful import abort
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from models import db
from views.blog_views import blog_bp
from views.user_views import user_bp

app = Flask(__name__)
app.secret_key = "kjsdkjjfhgukahyejfds"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

CORS(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.errorhandler(IntegrityError)
def title_not_unique():
  return {"message": "title not unique"}, 400


app.register_blueprint(blog_bp, url_prefix="/blog")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == "__main__":
  app.run(debug=True)
