from flask import Flask, render_template, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename


import json
from pymongo import MongoClient

client = MongoClient('mongodb://:@', )
db = client['admin']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEY'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received')

@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    #print('received event: ' + str(json))
    socketio.emit('res', json, callback=messageReceived)
    if json != {'data': 'User Connected'}:
        print(json['user_name'])
        print(json['message'])
        collection = db['test']
        collection.insert_one(json)

@app.route('/upload')
def render_file():
    return render_template('upload.html')

# 파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    print("upload_file")
    if request.method == 'POST':
        print("POST")
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save(secure_filename(f.filename))
        return f'<a href="http://filepile.xyz/chat/{f.filename}">http://filepile.xyz/chat/{f.filename}</a>'


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0' , debug=False, port=3000)
