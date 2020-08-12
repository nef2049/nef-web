import hashlib
import base64


def md5(file_name, block_size=64 * 1024):
    with open(file_name, 'rb') as f:
        _md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            _md5.update(data)
        _md5 = base64.b64encode(_md5.digest())
        return _md5
