import os
from flask import Flask, request, send_from_directory, jsonify, abort
import json

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('images', 'uploads')
PASSWORD = '852'  # 修改上传密码

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/upload', methods=['POST'])
def upload():
    if request.form.get('secret') != PASSWORD:
        return 'Forbidden', 403
    file = request.files.get('file')
    if not file:
        return 'No file', 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return 'OK', 200

@app.route('/list')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(sorted(files))

@app.route('/gallery')
def get_gallery():
    if not os.path.exists('gallery.json'):
        return jsonify([])
    with open('gallery.json', 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/save', methods=['POST'])
def save_image():
    data = request.get_json()
    if not data or 'url' not in data:
        return 'Bad Request', 400
    url = data['url']
    gallery = []
    if os.path.exists('gallery.json'):
        with open('gallery.json', 'r', encoding='utf-8') as f:
            gallery = json.load(f)
    if url not in gallery:
        gallery.append(url)
        with open('gallery.json', 'w', encoding='utf-8') as f:
            json.dump(gallery, f, ensure_ascii=False, indent=2)
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=8000)