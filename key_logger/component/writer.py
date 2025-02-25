from .interfaces import Writer
import json
import requests

class FileWriter(Writer):
    @staticmethod
    def send_data(data: str, path) -> None:
        with open(path, "w") as file:
            file.write(data)


class JsonWriter(Writer):
    @staticmethod
    def send_data(data: dict, path) -> None:
        with open(path, "w") as Json_File:
            json.dump(data, Json_File)


class NetworkWriter(Writer):
    @staticmethod
    def send_data(data):
        url = "http://127.0.0.1:5556/logs"
        headers = {"Content-Type": "application/json"}

        json_data = json.dumps(data)  # Convert to JSON string
        response = requests.post(url, json=data, headers=headers)  # ✅ Changed "data" to "json"

        return response.status_code


if __name__ == '__main__':
    pass
