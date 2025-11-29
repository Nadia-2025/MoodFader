from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  __tablename__="users"

id = db.Column(db.Integer, primary_key =True)
email = db.Column(db.String(120), unique =True, nullable=False)
username = db.Column(db.String(50), unique=True, nullable=False)
password_hash = db.Column(db.String, nullable=False)
created_at = db.Column(db.DateTime, primary_key =True)

favourites = db.relashionship("Favourite", backref="user", lazy=True)
moods = db.relashionship("Mood", backref="user", lazy=True)

def set_password(self,password):
  self.password_hash = generate_password_hash(password)

def check_password(self,password):
  return check_password_hash (self.password_hash, password)