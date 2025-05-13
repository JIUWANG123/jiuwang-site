from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

STATIC_DIR = 'static'
os.makedirs(STATIC_DIR, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    msg = db.Column(db.String(200))
    password = db.Column(db.String(100))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    question = db.Column(db.String(100))
    answer = db.Column(db.String(200))
    hidden = db.Column(db.Boolean, default=False)

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    time = db.Column(db.String(100))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        data = request.json
        if not data or 'msg' not in data:
            return 'Bad request', 400
        m = Message(name=data.get('name', '匿名'), msg=data['msg'], password=data.get('password', ''))
        db.session.add(m)
        db.session.commit()
        return '', 204
    all_messages = Message.query.all()
    return jsonify([{'name': m.name, 'msg': m.msg} for m in all_messages])

@app.route('/message/delete', methods=['POST'])
def message_delete():
    data = request.json
    msg = Message.query.get(int(data['index']))
    if msg and msg.password == data['pw']:
        db.session.delete(msg)
        db.session.commit()
    return '', 204

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        data = request.json
        if not data or 'question' not in data:
            return 'Bad request', 400
        name = '神秘人' if data.get('anonymous') else data.get('name', '匿名')
        q = Question(name=name, question=data['question'], answer='', hidden=False)
        db.session.add(q)
        db.session.commit()
        return '', 204
    all_questions = Question.query.all()
    return jsonify([
        {'name': q.name, 'question': q.question, 'answer': q.answer, 'hidden': q.hidden}
        for q in all_questions
    ])

@app.route('/question/reply', methods=['POST'])
def reply():
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    q = Question.query.get(int(data['index']))
    if q:
        q.answer = data['answer']
        db.session.commit()
    return '', 204

@app.route('/question/hide', methods=['POST'])
def hide():
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    q = Question.query.get(int(data['index']))
    if q:
        q.hidden = True
        db.session.commit()
    return '', 204

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = request.json
        if data.get('pw') != '852': return 'Forbidden', 403
        u = Update(content=data['content'], time=datetime.now().strftime('%Y-%m-%d %H:%M'))
        db.session.add(u)
        db.session.commit()
        return '', 204
    all_updates = Update.query.all()
    return jsonify([{'content': u.content, 'time': u.time} for u in all_updates])

@app.route('/update/delete', methods=['POST'])
def update_delete():
    data = request.json
    if data.get('pw') != '852': return 'Forbidden', 403
    u = Update.query.get(int(data['index']))
    if u:
        db.session.delete(u)
        db.session.commit()
    return '', 204

@app.route('/gallery', methods=['GET'])
def gallery():
    all_items = Gallery.query.all()
    return jsonify([g.url for g in all_items])

@app.route('/save', methods=['POST'])
def save_image():
    data = request.json
    g = Gallery(url=data['url'])
    db.session.add(g)
    db.session.commit()
    return '', 204

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
