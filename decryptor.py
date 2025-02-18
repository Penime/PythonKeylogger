def decrypt(data:bytes):
    if isinstance(data, str):
        data = data.encode('utf-8')
    key = b'KopLeoRos'
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))]).decode(errors='ignore')

print(decrypt('0e01133e1c1f26061c25'.encode('hex')))
    