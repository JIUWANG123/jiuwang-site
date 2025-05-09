import os
from flask import Flask, request, send_from_directory, jsonify, abort

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

if __name__ == '__main__':
    app.run(port=8000)
