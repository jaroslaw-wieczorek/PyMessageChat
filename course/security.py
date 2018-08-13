from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', '1234')
]

# after add User object
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


"""
before create user object
users = [
    {
        'id': 1,
        'username': 'bob',
        'password': '1234'
    }
]

username_mapping = { 'bob': {
        'id': 1,
        'username': 'bob',
        'password': '1234'
    }
}


userid_mapping = { 1: {
        'id': 1,
        'username': 'bob',
        'password': '1234'
    }
}


"""


def authenticate(username, password):
    # if user not exist return default value None
    user = username_mapping.get(username, None)
    # do not use this for operations
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    # payload is content of JWT
    user_id = payload['identity']
    # if user_id not exist return default value None
    return usrerid_mapping.get(user_id, None)
