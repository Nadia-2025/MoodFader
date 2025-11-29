
from flask import Blueprint, request, jsonify
from spotify import search_playlists_by_mood

mood_bp = Blueprint("mood_bp", __name__)

@mood_bp.route("/intro")
def intro():
  return jsonify ({"msg": "Hola!!!"})


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

# @bp.route('/callback')
# def callback():