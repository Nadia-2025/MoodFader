from database import db
from datetime import datetime

class Favourite(db.Model):
    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    playlist_id = db.Column(db.String(100), nullable=False)
    playlist_name = db.Column(db.String(150), nullable=False)
    playlist_url = db.Column(db.String(300), nullable=False)
    playlist_image = db.Column(db.String(300))
    mood_name = db.Column(db.String(50)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)