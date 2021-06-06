from . import db


class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False, unique=True)
  content = db.Column(db.Text, nullable=False)
  thumbnail = db.Column(db.Text, nullable=False)
  is_published = db.Column(db.Boolean, nullable=False,
                           default=False, server_default="0")
  author = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

  def __repr__(self) -> str:
    return "<Blog %r>" % self.title
