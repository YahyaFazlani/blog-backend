from flask import current_app
from werkzeug.utils import secure_filename


def create_filename(author, title, extension):
  return secure_filename(f"{author}_{title}_thumbnail.{extension}")


def file_allowed(filename: str):
  return '.' in filename and \
      filename.rsplit('.', 1)[1].lower(
      ) in current_app.config["ALLOWED_EXTENSIONS"]

