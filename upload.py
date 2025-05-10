from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/save', methods=['POST'])
def save_image():
    data = request.json
    url = data.get('url')
    if not url:
        return 'No URL provided', 400
    if not os.path.exists('data'):
        os.makedirs('data')
    with open('data/images.json', 'a', encoding='utf-8') as f:
        f.write(url + '\n')
    return 'OK'

@app.route('/gallery')
def gallery():
    try:
        with open('data/images.json', encoding='utf-8') as f:
            return jsonify([line.strip() for line in f.readlines() if line.strip()])
    except FileNotFoundError:
        return jsonify([])

@app.route('/message', methods=['GET', 'POST'])
def message():
    if not os.path.exists('data'):
        os.makedirs('data')
    path = 'data/messages.json'
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)

    if request.method == 'POST':
        data = request.json
        with open(path, encoding='utf-8') as f:
            messages = json.load(f)
        messages.append({
            'name': data.get('name', '匿名'),
            'msg': data.get('msg', ''),
            'pw': data.get('password', '')
        })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False)
        return 'OK'

    with open(path, encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/message/delete', methods=['POST'])
def delete_message():
    data = request.json
    index = int(data.get('index', -1))
    pw = data.get('pw', '')
    path = 'data/messages.json'
    with open(path, encoding='utf-8') as f:
        messages = json.load(f)
    if 0 <= index < len(messages) and messages[index].get('pw') == pw:
        messages.pop(index)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False)
    return 'OK'

@app.route('/question', methods=['GET', 'POST'])
def question():
    if not os.path.exists('data'):
        os.makedirs('data')
    path = 'data/questions.json'
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)

    if request.method == 'POST':
        data = request.json
        with open(path, encoding='utf-8') as f:
            questions = json.load(f)
        questions.append({
            'name': data.get('name', '匿名') if not data.get('anonymous') else '神秘人',
            'question': data.get('question', ''),
            'answer': '',
            'hidden': False
        })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False)
        return 'OK'

    with open(path, encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/question/reply', methods=['POST'])
def reply_question():
    data = request.json
    index = int(data.get('index', -1))
    answer = data.get('answer', '')
    pw = data.get('pw', '')
    if pw != '852': return 'Unauthorized', 403
    path = 'data/questions.json'
    with open(path, encoding='utf-8') as f:
        questions = json.load(f)
    if 0 <= index < len(questions):
        questions[index]['answer'] = answer
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False)
    return 'OK'

@app.route('/question/hide', methods=['POST'])
def hide_question():
    data = request.json
    index = int(data.get('index', -1))
    pw = data.get('pw', '')
    if pw != '852': return 'Unauthorized', 403
    path = 'data/questions.json'
    with open(path, encoding='utf-8') as f:
        questions = json.load(f)
    if 0 <= index < len(questions):
        questions[index]['hidden'] = True
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False)
    return 'OK'

@app.route('/update', methods=['GET', 'POST'])
def update():
    if not os.path.exists('data'):
        os.makedirs('data')
    path = 'data/updates.json'
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)

    if request.method == 'POST':
        data = request.json
        if data.get('pw') != '852':
            return 'Unauthorized', 403
        with open(path, encoding='utf-8') as f:
            updates = json.load(f)
        updates.insert(0, {
            'content': data.get('content', ''),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(updates, f, ensure_ascii=False)
        return 'OK'

    with open(path, encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/update/delete', methods=['POST'])
def delete_update():
    data = request.json
    index = int(data.get('index', -1))
    pw = data.get('pw', '')
    if pw != '852': return 'Unauthorized', 403
    path = 'data/updates.json'
    with open(path, encoding='utf-8') as f:
        updates = json.load(f)
    if 0 <= index < len(updates):
        updates.pop(index)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(updates, f, ensure_ascii=False)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)