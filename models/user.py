from . import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(255), nullable=False)
  lastname = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(320), unique=True, nullable=False)
  password = db.Column(db.String(256), nullable=False)
  blogs = db.relationship("Blog", backref=db.backref("user"), lazy=True)

  def __repr__(self) -> str:
    return "<User %r>" % f"'{self.firstname} {self.lastname}'"
