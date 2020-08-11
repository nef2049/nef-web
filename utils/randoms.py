import random


def random_digital(length=20):
    num = ''
    chars = '1234567890'
    _length = len(chars) - 1
    rd = random.Random()
    for j in range(length):
        num += chars[rd.randint(0, _length)]
    return int(num)

def random_chars(length=20):
    result = ''
    chars = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _length = len(chars) - 1
    rd = random.Random()
    for j in range(length):
        result += chars[rd.randint(0, _length)]
    return result


if __name__ == "__main__":
    print(random_chars())