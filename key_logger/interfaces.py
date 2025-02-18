from abc import ABC, abstractmethod


class KeyLogger(ABC):
    @abstractmethod
    def start_logging(self) -> None:
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        pass

    @abstractmethod
    def get_logged_keys(self) -> list[str]:
        pass


class Writer(ABC):
    @abstractmethod
    def send_data(self, data: dict) -> None:
        pass


class Encyptor(ABC):
    @abstractmethod
    def encrypt(self, data: str):
        pass
