from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(255), nullable=False)
  lastname = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(320), unique=True, nullable=False)
  password = db.Column(db.String(256), nullable=False)
  blogs=db.relationship("Blog", backref = db.backref("user"), lazy = True)

  def __repr__(self) -> str:
    return "<User %r>" % f"'{self.firstname} {self.lastname}'"


class Blog(db.Model):
  id=db.Column(db.Integer, primary_key = True)
  title=db.Column(db.String(100), nullable = False, unique = True)
  content=db.Column(db.Text, nullable = False)
  is_published=db.Column(db.Boolean, nullable = False,
                           default = False, server_default = "0")
  author=db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

  def __repr__(self) -> str:
    return "<Blog %r>" % self.title
