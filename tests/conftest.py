from flask.testing import FlaskClient
import pytest
from app import create_app
from models import db


class AuthActions(object):
  def __init__(self, client: FlaskClient) -> None:
    self._client = client

  def register(self, firstname="Test", lastname="User", email="testuser@test.com", password="supersecret"):
    data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": password
    }

    response = self._client.post("/auth/register", data=data)

    return response

  def login(self, email="testuser@test.com", password="supersecret"):
    data = {
        "email": email,
        "password": password
    }

    response = self._client.post("/auth/login", data=data)

    return response


@pytest.fixture(scope="package")
def client():
  app = create_app(config="configs.TestingConfig")

  with app.test_client() as client:
    with app.app_context():
      db.create_all()
    yield client


@pytest.fixture(scope="module")
def auth(client):
  return AuthActions(client)
