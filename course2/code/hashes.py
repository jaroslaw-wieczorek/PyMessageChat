import random
import string
import hashlib


def randomData(length=64):
    return ''.join(random.sample(string.ascii_letters +
                                 string.digits +
                                 string.punctuation, length))

def hashData(data, salt=''):
    data = data.join(salt)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
