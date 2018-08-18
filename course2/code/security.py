from werkzeug.security import safe_str_cmp
from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user is not None and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    # payload is content of JWT
    user_id = payload['identity']
    # if user_id not exist return default value None
    return User.find_by_id(user_id)
