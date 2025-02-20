from interfaces import Writer

class FileWriter(Writer):
    @staticmethod
    def send_data(data:str, path) -> None:
        with open(path ,"a") as file:
            file.write(data)


class JsonWriter(Writer):
    @staticmethod
    def send_data(data: dict):
        pass


class NetworkWriter(Writer):
    @staticmethod
    def send_data(data):
        pass


if __name__ == '__main__':
    FileWriter.send_data()