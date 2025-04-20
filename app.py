from flask import Flask, request, jsonify, send_from_directory, render_template_string
import json
import os

app = Flask(__name__)

POINTS_FILE = 'points.json'
BEHAVIORS_FILE = 'behaviors.json'
CHILDREN = [
    {"id": "clara", "name": "Clara Zhang", "cn": "张予"},
    {"id": "cramer", "name": "Cramer Zhang", "cn": "张晏"}
]

# Load points data
if os.path.exists(POINTS_FILE):
    with open(POINTS_FILE, 'r', encoding='utf-8') as f:
        points = json.load(f)
else:
    points = {child['name']: 0 for child in CHILDREN}

# Load behaviors data from JSON file
if os.path.exists(BEHAVIORS_FILE):
    with open(BEHAVIORS_FILE, 'r', encoding='utf-8') as f:
        behaviors = json.load(f)
else:
    behaviors = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory('static', 'index.html')

@app.route('/behaviors.html')
def behaviors_page():
    return send_from_directory('static', 'behaviors.html')

@app.route('/behaviors_by_frequency.html')
def behaviors_by_frequency_page():
    return send_from_directory('static', 'behaviors_by_frequency.html')

@app.route('/edit_behaviors.html')
def edit_behaviors_page():
    return send_from_directory('static', 'edit_behaviors.html')

@app.route('/children', methods=['GET'])
def get_children():
    """Get all children info"""
    return jsonify(CHILDREN)

@app.route('/points', methods=['GET'])
def get_points():
    """Return points for all valid children"""
    return jsonify({child['name']: points.get(child['name'], 0) for child in CHILDREN})

@app.route('/points/<child>', methods=['POST'])
def add_points(child):
    """Add points for a specific child, body: {"amount": 5}"""
    # Only allow valid children
    valid_names = [c['name'] for c in CHILDREN]
    if child not in valid_names:
        return jsonify({"error": "Invalid child name"}), 400
    data = request.get_json()
    amount = data.get('amount', 0)
    points[child] = points.get(child, 0) + amount
    # Persist data
    with open(POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(points, f, ensure_ascii=False)
    return jsonify({child: points[child]})

@app.route('/behaviors', methods=['GET', 'POST'])
def behaviors_api():
    """Get or update all behaviors with points"""
    global behaviors
    if request.method == 'GET':
        return jsonify(behaviors)
    elif request.method == 'POST':
        behaviors = request.get_json()
        with open(BEHAVIORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(behaviors, f, ensure_ascii=False, indent=4)
        return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
