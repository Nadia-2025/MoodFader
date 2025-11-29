from flask import Blueprint, request, jsonify
from spotify import search_playlists_by_mood
from database import db
from models.mood import Mood
from models.users import User
import jwt
import os

mood_bp = Blueprint("mood_bp", __name__)
SECRET_KEY = os.getenv("SECRET_KEY")

@mood_bp.route('/mood', methods=['GET'])
def get_mood_playlists():

    mood = request.args.get('emotion')

    if not mood:
        return jsonify({"error": "No emotion provided"}), 400

    playlists = search_playlists_by_mood(mood)

    return jsonify({
        "emotion": mood,
        "playlists": playlists
    })

@mood_bp.route("/mood/save", methods=["POST"])
def save_mood():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401

    data = request.json
    mood_name = data.get("mood_name")
    if not mood_name:
        return jsonify({"error": "Mood name required"}), 400

    new_mood = Mood(user_id=user_id, mood_name=mood_name)
    db.session.add(new_mood)
    db.session.commit()

    return jsonify({"message": "Mood saved successfully"})

# @bp.route('/callback')
# def callback():