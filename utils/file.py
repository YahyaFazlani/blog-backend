from flask import current_app
from werkzeug.utils import secure_filename
from typing import Optional


def get_extension(filename: Optional[str]):
  return filename.rsplit('.', 1)[1].lower()


def create_filename(author, title, extension):
  return secure_filename(f"{author}_{title}_thumbnail.{extension}")


def is_allowed(filename: Optional[str]):
  return filename is not None and '.' in filename and \
      filename.endswith(current_app.config["ALLOWED_EXTENSIONS"])
