import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth_routes import auth_bp
from routes.moods_routes import mood_bp
from routes.favourites_routes import favourites_bp
from database import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodfader.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(mood_bp, url_prefix="/api")
app.register_blueprint(favourites_bp, url_prefix="/api")

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.get("/api/saludo")
def saludo():
    return jsonify({"message": "MoodFader loading..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True)