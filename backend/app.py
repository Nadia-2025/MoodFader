import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes import bp
from database import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodfader.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
app.register_blueprint(bp, url_prefix="/api")

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.get("/api/saludo")
def saludo():
    return jsonify({"message": "MoodFader loading..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True)