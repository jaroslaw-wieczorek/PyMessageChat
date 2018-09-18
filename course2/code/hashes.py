import random
import string
import hashlib


def randomData(length=64):
    return ''.join(random.sample(string.ascii_letters +
                                 string.digits +
                                 string.punctuation, length))


def hashData(data, specific_data=''):
    data2 = str(data) + str(specific_data)
    return hashlib.sha256(data2.encode("utf-8")).hexdigest()
