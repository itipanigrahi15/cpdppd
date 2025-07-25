from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# Initialize or load existing data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"entries": []}, f)

with open(DATA_FILE) as f:
    data = json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/entries", methods=["GET"])
def get_entries():
    return jsonify(data["entries"])

@app.route("/api/entries", methods=["POST"])
def add_entry():
    entry = request.get_json()
    entry["date"] = datetime.now().strftime("%Y-%m-%d")
    entry["status"] = entry.get("status", "Pending")  # ✅ Accept status from frontend
    data["entries"].append(entry)
    save_data()
    return jsonify(entry), 201

if __name__ == "__main__":
    app.run(debug=True)
