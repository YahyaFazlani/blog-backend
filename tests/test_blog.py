from tests.conftest import AuthActions
from flask.testing import FlaskClient


def test_post_blog(client: FlaskClient, auth: AuthActions):
  user_response = auth.login()
  user_response_status = user_response.status_code
  user_response_json = user_response.json
  assert user_response_status == 200

  access_token = user_response_json["access_token"]
  filename = "test_image.jpg"
  filepath = f"tests/{filename}"

  blog_data = {
      "title": "Test Blog",
      "content": "Test content",
      "thumbnail": (open(filepath, "rb"), "test_image.jpg"),
      "is_published": True
  }
  blog_headers = {
      "Authorization": f"Bearer {access_token}"
  }

  blog_response = client.post("/blog/", data=blog_data, headers=blog_headers)
  assert blog_response.status_code == 201
