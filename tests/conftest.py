import pytest
from app import create_app
from models import db
from models.blog import Blog
from models.user import User


@pytest.fixture(scope="module")
def client():
  app = create_app
  app.testing = True
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
  db.init_app(app)

  with app.test_client() as client:
    with app.app_context():
      db.create_all()

      for i in range(1, 5):
        test_user = User(firstname=f"TestUser{i}", lastname="Blogger",
                         email=f"testuser{i}@outlook.com", password="jfkdlsajfklds")
        db.session.add(test_user)
        db.session.commit()
    yield client
