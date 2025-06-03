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
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/message', methods=['GET', 'POST'])
def message():
    path = os.path.join(DATA_DIR, 'messages.json')
    if request.method == 'POST':
        try:
            data = request.json
            print('收到留言:', data)
            if not data or 'msg' not in data:
                return 'Bad request', 400
            messages = read_json(path)
            messages.append({
                'name': data.get('name', '匿名'),
                'msg': data['msg'],
                'password': data.get('password', '')
            })
            write_json(path, messages)
            return '', 204
        except Exception as e:
            print('留言提交错误:', str(e))
            return 'Server error', 500
    return jsonify(read_json(path))

@app.route('/message/delete', methods=['POST'])
def message_delete():
    path = os.path.join(DATA_DIR, 'messages.json')
    data = request.json
    messages = read_json(path)
    try:
        index = int(data['index'])
        if messages[index]['password'] == data['pw']:
            messages.pop(index)
            write_json(path, messages)
    except: pass
    return '', 204

@app.route('/question', methods=['GET', 'POST'])
def question():
    path = os.path.join(DATA_DIR, 'questions.json')
    if request.method == 'POST':
        try:
            data = request.json
            print('收到提问:', data)
            if not data or 'question' not in data:
                return 'Bad request', 400
            name = '神秘人' if data.get('anonymous') else data.get('name', '匿名')
            questions = read_json(path)
            questions.append({
                'name': name,
                'question': data['question'],
                'answer': '',
                'hidden': False
            })
            write_json(path, questions)
            return '', 204
        except Exception as e:
            print('提问提交错误:', str(e))
            return 'Server error', 500
    return jsonify(read_json(path))

@app.route('/question/reply', methods=['POST'])
def reply():
    path = os.path.join(DATA_DIR, 'questions.json')
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    questions = read_json(path)
    questions[int(data['index'])]['answer'] = data['answer']
    write_json(path, questions)
    return '', 204

@app.route('/question/hide', methods=['POST'])
def hide():
    path = os.path.join(DATA_DIR, 'questions.json')
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    questions = read_json(path)
    questions[int(data['index'])]['hidden'] = True
    write_json(path, questions)
    return '', 204

@app.route('/update', methods=['GET', 'POST'])
def update():
    path = os.path.join(DATA_DIR, 'updates.json')
    if request.method == 'POST':
        data = request.json
        if data.get('pw') != '852': return 'Forbidden', 403
        items = read_json(path)
        items.append({'content': data['content'], 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
        write_json(path, items)
        return '', 204
    return jsonify(read_json(path))

@app.route('/update/delete', methods=['POST'])
def update_delete():
    path = os.path.join(DATA_DIR, 'updates.json')
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    items = read_json(path)
    try: items.pop(int(data['index']))
    except: pass
    write_json(path, items)
    return '', 204

@app.route('/gallery', methods=['GET'])
def gallery():
    path = os.path.join(DATA_DIR, 'gallery.json')
    return jsonify(read_json(path))

@app.route('/save', methods=['POST'])
def save_image():
    path = os.path.join(DATA_DIR, 'gallery.json')
    data = request.json
    items = read_json(path)
    items.append(data['url'])
    write_json(path, items)
    return '', 204

@app.route('/gallery/edit', methods=['POST'])
def edit_gallery():
    path = os.path.join(DATA_DIR, 'gallery.json')
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    index = int(data['index'])
    field = data['field']
    value = data['value']
    gallery = read_json(path)
    if isinstance(gallery[index], dict):
        gallery[index][field] = value
    else:
        gallery[index] = {field: value, 'url': gallery[index]}
    write_json(path, gallery)
    return '', 204

@app.route('/gallery/delete', methods=['POST'])
def delete_gallery():
    path = os.path.join(DATA_DIR, 'gallery.json')
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    gallery = read_json(path)
    try:
        gallery.pop(int(data['index']))
    except:
        pass
    write_json(path, gallery)
    return '', 204

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
