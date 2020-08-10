import uuid


def uuid_mac():
    return str(uuid.uuid1()).replace('-', '')


def uuid_ramdom():
    return str(uuid.uuid4()).replace('-', '')
