
# Reprezentation of user
import sqlite3
from flask_restful import reqparse
from flask_restful import Resource


class User:

    def __init__(self, _db_id, _id, username, password):
        # used _id because id is python keyword than self.id.
        self.db_id = _db_id
        self.id = _id
        self.username = username
        self.password = password

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

        query = "SELECT * FROM users WHERE user_id=?"
        result = cursor.execute(query, (_id,))  # arg must be tuple
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Create user ID for app
        #
        data.update({"user_id": data['username'] + "_id"})
        #
        #
        query = "INSERT INTO users (id, user_id, username, password) \
                 VALUES (NULL, ?, ?, ?)"

        cursor.execute(query, (data['user_id'],
                               data['username'],
                               data['password'])
                       )

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
