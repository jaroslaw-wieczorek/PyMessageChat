from werkzeug.security import safe_str_cmp
from resources.user import UserModel

import random
import string
import hashlib



def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    # payload is content of JWT
    user_id = payload['identity']
    # if user_id not exist return default value None
    return UserModel.find_by_id(user_id)


def randomRubbish(length=64):
    return ''.join(random.sample(string.ascii_letters +
                                 string.digits +
                                 string.punctuation, length))


def hashRubbish(trash):
    return hashlib.sha256(trash.encode()).hexdigest()
