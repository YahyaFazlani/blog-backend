from tests.conftest import AuthActions
from flask.testing import FlaskClient

from models.user import User


def test_register(auth: AuthActions):
  auth.register()

  assert User.query.get(1)
