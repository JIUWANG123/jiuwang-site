
from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 路径设置
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
UPDATE_FILE = os.path.join(DATA_DIR, 'updates.json')
QUESTION_FILE = os.path.join(DATA_DIR, 'questions.json')

# 读取 JSON 文件
def read_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 写入 JSON 文件
def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = request.json
        if data.get('pw') != '852': return 'Forbidden', 403
        updates = read_json(UPDATE_FILE)
        updates.append({
            'content': data['content'],
            'time': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        write_json(UPDATE_FILE, updates)
        return '', 204
    return jsonify(read_json(UPDATE_FILE))

@app.route('/update/delete', methods=['POST'])
def delete_update():
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    updates = read_json(UPDATE_FILE)
    try:
        updates.pop(int(data['index']))
    except: pass
    write_json(UPDATE_FILE, updates)
    return '', 204
