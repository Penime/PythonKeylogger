from interfaces import Writer


class FileWriter(Writer):
    def __init__(self):
        pass

    def send_data(self, data):
        pass


class JsonWriter(Writer):
    def __init__(self):
        pass

    def send_data(self, data: dict):
        pass


class NetworkWriter(Writer):
    def __init__(self):
        pass

    def send_data(self, data: str | dict):
        pass
