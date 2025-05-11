
from flask import Flask, request, jsonify, send_from_directory
import os, json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_DIR = 'data'
STATIC_DIR = 'static'
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def read_json(path):
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

@app.route('/about', methods=['GET', 'POST'])
def about():
    path = os.path.join(DATA_DIR, 'about.txt')
    if request.method == 'POST':
        data = request.json
        if data.get('pw') != '852': return 'Forbidden', 403
        write_text(path, data.get('content', ''))
        return '', 204
    return read_json(path), 200

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
