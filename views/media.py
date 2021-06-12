from flask import send_from_directory


def media(path):
  return send_from_directory("media", path)
