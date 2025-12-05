from flask import Blueprint, request, jsonify
from database import db
from models.favourites import Favourite
import jwt
import os

favourites_bp = Blueprint("favourites_bp", __name__)
SECRET_KEY = os.getenv("SECRET_KEY")

@favourites_bp.route("/favourites", methods=["GET"])
def get_favourites():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except:
        return jsonify({"error": "Invalid token"}), 401

    favs = Favourite.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": f.id,
        "playlist_name": f.playlist_name,
        "playlist_url": f.playlist_url,
        "playlist_image": f.playlist_image,
        "mood_name": f.mood_name
    } for f in favs])

@favourites_bp.route("/favourites/add", methods=["POST"])
def add_favourite():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except:
        return jsonify({"error": "Invalid token"}), 401

    data = request.json
    required_fields = ["playlist_id", "playlist_name", "playlist_url"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing playlist data"}), 400

    new_fav = Favourite(
        user_id=user_id,
        playlist_id=data["playlist_id"],
        playlist_name=data["playlist_name"],
        playlist_url=data["playlist_url"],
        playlist_image=data.get("playlist_image"),
        mood_name=data.get("mood_name")
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "Favourite added successfully"})

@favourites_bp.route("/favourites/<int:fav_id>", methods=["DELETE"])
def delete_favourite(fav_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except:
        return jsonify({"error": "Invalid token"}), 401

    fav = Favourite.query.filter_by(id=fav_id, user_id=user_id).first()
    if not fav:
        return jsonify({"error": "Favourite not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favourite deleted successfully"})
