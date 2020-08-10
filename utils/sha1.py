import hashlib
import base64


def sha1(file_name, block_size=64 * 1024):
    with open(file_name, 'rb') as f:
        _sha1 = hashlib.sha1()
        while True:
            data = f.read(block_size)
            if not data:
                break
            _sha1.update(data)
        _sha1 = base64.b64encode(_sha1.digest())
        return _sha1
