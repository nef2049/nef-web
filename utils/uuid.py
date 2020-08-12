import uuid


def uuid_mac():
    return str(uuid.uuid1()).replace('-', '')


def uuid_random():
    return str(uuid.uuid4()).replace('-', '')
