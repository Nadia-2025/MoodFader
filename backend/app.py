import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes import bp

load_dotenv()

app = Flask(__name__)
CORS(app)
app.register_blueprint(bp, url_prefix="/api")

@app.get("/api/saludo")
def saludo():
    return jsonify({"message": "MoodFader loading..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True)