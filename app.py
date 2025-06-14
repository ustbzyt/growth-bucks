from flask import Flask, request, jsonify, send_from_directory, render_template_string
import json
import os
import datetime

app = Flask(__name__)

POINTS_FILE = 'points.json'
BEHAVIORS_FILE = 'behaviors.json'
CHILDREN = [
    {"id": "clara", "name": "Clara Zhang", "cn": "张予"},
    {"id": "cramer", "name": "Cramer Zhang", "cn": "张晏"}
]

def get_current_week_key():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday() + 1 if today.weekday() < 6 else 0)
    end = start + datetime.timedelta(days=6)
    return f"{start.isoformat()}~{end.isoformat()}"

# Load points data
if os.path.exists(POINTS_FILE):
    with open(POINTS_FILE, 'r', encoding='utf-8') as f:
        points = json.load(f)
else:
    points = {child['name']: {"total": 0, "weekly": 0, "week_key": get_current_week_key()} for child in CHILDREN}

def reset_weekly_points_if_needed():
    week_key = get_current_week_key()
    changed = False
    for child in CHILDREN:
        name = child['name']
        if name not in points or not isinstance(points[name], dict):
            points[name] = {"total": 0, "weekly": 0, "week_key": week_key}
            changed = True
        elif points[name].get("week_key") != week_key:
            points[name]["weekly"] = 0
            points[name]["week_key"] = week_key
            changed = True
    if changed:
        with open(POINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(points, f, ensure_ascii=False, indent=4)

# Load behaviors data from JSON file
if os.path.exists(BEHAVIORS_FILE):
    with open(BEHAVIORS_FILE, 'r', encoding='utf-8') as f:
        behaviors = json.load(f)
else:
    behaviors = []

REDEMPTIONS_FILE = 'redemptions.json'
POINTS_HISTORY_FILE = 'points_history.json'

# 加载兑换历史
if os.path.exists(REDEMPTIONS_FILE):
    with open(REDEMPTIONS_FILE, 'r', encoding='utf-8') as f:
        redemptions = json.load(f)
else:
    redemptions = {}

# 加载每周积分历史
if os.path.exists(POINTS_HISTORY_FILE):
    with open(POINTS_HISTORY_FILE, 'r', encoding='utf-8') as f:
        points_history = json.load(f)
else:
    points_history = {}

# --- 新增：启动时同步本周积分到历史 ---
def sync_points_history_with_current():
    week_key = get_current_week_key()
    changed = False
    for child in CHILDREN:
        name = child['name']
        weekly_points = points.get(name, {}).get('weekly', 0)
        if name not in points_history:
            points_history[name] = []
        # 如果本周没有记录，则追加
        if not any(item['week'] == week_key for item in points_history[name]):
            points_history[name].append({'week': week_key, 'points': weekly_points})
            changed = True
        # 如果本周有记录但分数不一致，则更新
        else:
            for item in points_history[name]:
                if item['week'] == week_key and item['points'] != weekly_points:
                    item['points'] = weekly_points
                    changed = True
    if changed:
        with open(POINTS_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(points_history, f, ensure_ascii=False, indent=4)

# --- 在加载完 points_history 后立即同步 ---
sync_points_history_with_current()

# 每周积分历史自动记录（可在每次 get_points 时调用）
def update_points_history():
    week_key = get_current_week_key()
    for child in CHILDREN:
        name = child['name']
        if name not in points_history:
            points_history[name] = []
        # 检查是否已有本周记录
        if not any(item['week'] == week_key for item in points_history[name]):
            points_history[name].append({'week': week_key, 'points': points[name]['weekly']})
            with open(POINTS_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(points_history, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory('static', 'index.html')

@app.route('/behaviors_by_frequency.html')
def behaviors_by_frequency_page():
    return send_from_directory('static', 'behaviors_by_frequency.html')

@app.route('/edit_behaviors.html')
def edit_behaviors_page():
    return send_from_directory('static', 'edit_behaviors.html')

@app.route('/behaviors_by_category.html')
def behaviors_by_category():
    print("Current working directory:", os.getcwd())
    print("File exists:", os.path.exists(os.path.join('static', 'behaviors_by_category.html')))
    return send_from_directory('static', 'behaviors_by_category.html')

@app.route('/allowance.html')
def allowance_page():
    return send_from_directory('static', 'allowance.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/sounds/<path:filename>')
def serve_sound(filename):
    return send_from_directory('static/sounds', filename)

@app.route('/children', methods=['GET'])
def get_children():
    """Get all children info"""
    return jsonify(CHILDREN)

@app.route('/points', methods=['GET'])
def get_points():
    reset_weekly_points_if_needed()
    update_points_history()
    return jsonify({child['name']: {
        "total": points[child['name']]["total"],
        "weekly": points[child['name']]["weekly"]
    } for child in CHILDREN})

@app.route('/points/<child>', methods=['POST'])
def add_points(child):
    reset_weekly_points_if_needed()
    valid_names = [c['name'] for c in CHILDREN]
    if child not in valid_names:
        return jsonify({"error": "Invalid child name"}), 400
    
    data = request.get_json()
    amount = data.get('amount', 0)
    behavior_name = data.get('behavior') # 获取行为名称

    # 更新积分
    points[child]["total"] += amount
    points[child]["weekly"] += amount

    # 如果是兑换行为（负分且有behavior_name），则记录
    if amount < 0 and behavior_name:
        if child not in redemptions:
            redemptions[child] = []
        
        # 从 behaviors.json 中查找对应的描述
        behavior_info = next((b for b in behaviors if b['name'] == behavior_name), None)
        desc = behavior_info['desc'] if behavior_info else behavior_name

        redemptions[child].append({
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'points': -amount, # 记录为正数
            'desc': desc
        })
        with open(REDEMPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(redemptions, f, ensure_ascii=False, indent=4)

    # 持久化积分数据
    with open(POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(points, f, ensure_ascii=False, indent=4)
        
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

@app.route('/allowance/<child>')
def get_allowance(child):
    if child not in points:
        return jsonify({'error': 'Child not found'}), 404
    return jsonify({'allowance': points[child].get('allowance', 0)})

@app.route('/redemptions/<child>')
def get_redemptions(child):
    return jsonify(redemptions.get(child, []))

@app.route('/points_history/<child>')
def get_points_history(child):
    return jsonify(points_history.get(child, []))

if __name__ == '__main__':
    app.run(debug=True)