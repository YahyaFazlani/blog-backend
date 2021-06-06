import pytest
from app import app
from models import db
from models.user import User
from models.blog import Blog


@pytest.fixture(scope="module")
def client():
  app.testing = True
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
  db.init_app(app)

  with app.test_client() as client:
    with app.app_context():
      db.create_all()

      for i in range(1, 5):
        test_user = User(firstname=f"TestUser{i}", lastname="Blog",
                         email=f"testuser{i}@outlook.com", password="jfkdlsajfklds")
        db.session.add(test_user)
        db.session.commit()
    yield client
