from interfaces import Writer

class FileWriter(Writer):
    # def __init__(self):
    #     pass

    @staticmethod
    def send_data(data:str, path):
        with open(path ,"a") as file:
            file.write (data)


class JsonWriter(Writer):
    # def __init__(self):
    #     pass

    def send_data(self, data: dict):
        pass


class NetworkWriter(Writer):
    # def __init__(self):
    #     pass

    def send_data(self, data):
        pass


if __name__ == '__main__':
    FileWriter.send_data()