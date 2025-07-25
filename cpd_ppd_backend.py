from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Set file paths relative to current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRIES_FILE = os.path.join(BASE_DIR, 'entries.json')
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

@app.route('/')
def home():
    return "CPD/PPD API is running."

@app.route('/entries', methods=['GET'])
def get_entries():
    if not os.path.exists(ENTRIES_FILE):
        return jsonify([])
    with open(ENTRIES_FILE, 'r') as f:
        entries = json.load(f)
    return jsonify(entries)

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify([])
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    new_entry = request.get_json()
    if not new_entry:
        return jsonify({"error": "No data provided"}), 400

    # Load existing entries
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, 'r') as f:
            entries = json.load(f)
    else:
        entries = []

    entries.append(new_entry)

    with open(ENTRIES_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

    return jsonify({'status': 'success', 'entry': new_entry}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
