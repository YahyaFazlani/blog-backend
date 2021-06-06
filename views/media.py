from flask import Blueprint, send_from_directory

media_bp = Blueprint("media", __name__, url_prefix="/media/")


@media_bp.route("/<path:path>")
def media(path):
  return send_from_directory("media", path)
