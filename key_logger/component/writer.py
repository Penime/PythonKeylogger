from interfaces import Writer
import json
class FileWriter(Writer):
    @staticmethod
    def send_data(data:str, path) -> None:
        with open(path ,"w") as file:
            file.write(data)


class JsonWriter(Writer):
    @staticmethod
    def send_data(data: dict, path):
        with open (path , "w") as Json_File:
            json.dump(data)


class NetworkWriter(Writer):
    @staticmethod
    def send_data(data):
        pass


if __name__ == '__main__':
    FileWriter.send_data()