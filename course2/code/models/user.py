import sqlite3


class UserModel:

    def __init__(self, _id, username, password, email, picture, status):
        # used _id because id is python keyword than self.id.
        self.id = _id
        self.email = email
        self.username = username
        self.password = password
        self.picture = picture
        self.status = status

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # arg must be tuple
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM users WHERE user_id=?"""
        result = cursor.execute(query, (_id,))  # arg must be tuple
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
