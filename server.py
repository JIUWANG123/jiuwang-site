from flask import Flask, send_from_directory
from upload import app as upload_app

app = upload_app

@app.route('/')
def index():
    return send_from_directory('', 'index.html')
