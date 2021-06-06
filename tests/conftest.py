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
      user = User(firstname="Yahya", lastname="Fazlani", email="yahyafazlani@outlook.com", password="yahyafazlani@outlook.com")
      db.session.add(user)
      db.session.commit()
      blog = Blog(title="Test", content="test", thumbnail="htctps://google.com/", is_published=True, author=user.id)
      db.session.add(blog)
      db.session.commit()
    yield client
