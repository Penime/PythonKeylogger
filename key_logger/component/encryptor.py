from interfaces import Encyptor


class XorEcryptor(Encyptor):
    def __init__(self, key='KopLeoRos') -> None:
        self.__key = key.encode()

    def encrypt(self, data: str | dict) -> bytes:
        data = str(data).encode()
        return bytes([data[i] ^ self.__key[i % len(self.__key)] for i in range(len(data))])


if __name__ == '__main__':
    x = XorEcryptor()
    with open('encrypted_data.txt', 'wb') as file:
        file.write(x.encrypt('Encryption'))
