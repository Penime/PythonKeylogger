def decrypt(path: str) -> bytes:
    key = b'KopLeoRos'
    with open(path, 'rb') as file:
        data: bytes = file.read()
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])


print(decrypt('encrypted_data.txt'))
