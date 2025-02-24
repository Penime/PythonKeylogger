from .interfaces import Writer
import json
import requests

class FileWriter(Writer):
    @staticmethod
    def send_data(data:str, path) -> None:
        with open(path ,"w") as file:
            file.write(data)


class JsonWriter(Writer):
    @staticmethod
    def send_data(data: dict, path) -> None:
        with open (path , "w") as Json_File:
            json.dump(data)


class NetworkWriter(Writer):
    @staticmethod
    def send_data(data) -> int:
        url = "http://127.0.0.1:5556/logs"
        response = requests.post(url, data=data)

        return response.status_code


if __name__ == '__main__':
    pass
