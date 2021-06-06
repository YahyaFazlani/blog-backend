from flask import Blueprint
from sqlalchemy.exc import IntegrityError

error_bp = Blueprint("errors", __name__)

@error_bp.app_errorhandler(IntegrityError)
def title_not_unique():
  return {"message": "title not unique"}, 400
