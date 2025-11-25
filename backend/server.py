from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/api/intro")
def intro():
    return jsonify({"message": "MoodFader loading..."})

if __name__ == "__main__":
    app.run(debug=True)