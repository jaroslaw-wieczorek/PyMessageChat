class User:
    def __init__(self, _id, username, password):
        # used _id because id is python keyword than self.id.
        self.id = _id
        self.username = username
        self.password = password
