def decrypt_file(path: str, key='KopLeoRos') -> bytes:
    key: bytes = key.encode()
    with open(path, 'rb') as file:
        data: bytes = file.read()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])


print(decrypt_file('encrypted_data.txt'))
