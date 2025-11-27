from flask import Blueprint, jsonify

bp = Blueprint("routes_bp", __name__)

@bp.route("/intro")
def intro():
  return jsonify ({"msg": "Hola!!!"})


# @app.route('/callback')
# def callback():