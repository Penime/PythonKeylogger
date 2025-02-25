
def decrypt_data(data: bytes, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
