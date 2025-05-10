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


@app.route('/message', methods=['GET'])
def get_messages():
    if not os.path.exists('messages.json'):
        return jsonify([])
    with open('messages.json', 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/message', methods=['POST'])
def post_message():
    data = request.get_json()
    if not data or 'msg' not in data or 'name' not in data:
        return 'Bad Request', 400
    new_entry = {'name': data['name'], 'msg': data['msg']}
    messages = []
    if os.path.exists('messages.json'):
        with open('messages.json', 'r', encoding='utf-8') as f:
            messages = json.load(f)
    messages.append(new_entry)
    with open('messages.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    return 'OK', 200

@app.route('/message/delete', methods=['POST'])
def delete_message():
    data = request.get_json()
    if not data or 'index' not in data or 'pw' not in data:
        return 'Bad Request', 400
    if data['pw'] != '852':
        return 'Forbidden', 403
    try:
        index = int(data['index'])
        with open('messages.json', 'r', encoding='utf-8') as f:
            messages = json.load(f)
        if 0 <= index < len(messages):
            messages.pop(index)
            with open('messages.json', 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
        return 'OK', 200
    except Exception:
        return 'Error', 500

if __name__ == '__main__':

# 提问箱相关
@app.route('/question', methods=['GET'])
def get_questions():
    if not os.path.exists('questions.json'):
        return jsonify([])
    with open('questions.json', 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/question', methods=['POST'])
def post_question():
    data = request.get_json()
    if not data or 'question' not in data or 'name' not in data:
        return 'Bad Request', 400
    name = data['name']
    if data.get('anonymous'):
        name = '神秘人：'
    new_entry = {
        'name': name,
        'question': data['question'],
        'answer': '',
        'hidden': False
    }
    questions = []
    if os.path.exists('questions.json'):
        with open('questions.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    questions.append(new_entry)
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    return 'OK', 200

@app.route('/question/reply', methods=['POST'])
def reply_question():
    data = request.get_json()
    if not data or 'index' not in data or 'answer' not in data or 'pw' not in data:
        return 'Bad Request', 400
    if data['pw'] != '852':
        return 'Forbidden', 403
    try:
        index = int(data['index'])
        with open('questions.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
        if 0 <= index < len(questions):
            questions[index]['answer'] = data['answer']
            with open('questions.json', 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
        return 'OK', 200
    except Exception:
        return 'Error', 500

@app.route('/question/hide', methods=['POST'])
def hide_question():
    data = request.get_json()
    if not data or 'index' not in data or 'pw' not in data:
        return 'Bad Request', 400
    if data['pw'] != '852':
        return 'Forbidden', 403
    try:
        index = int(data['index'])
        with open('questions.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
        if 0 <= index < len(questions):
            questions[index]['hidden'] = True
            with open('questions.json', 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
        return 'OK', 200
    except Exception:
        return 'Error', 500