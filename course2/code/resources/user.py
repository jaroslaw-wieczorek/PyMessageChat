# Reprezentation of user
import sys
import sqlite3

from models.user import UserModel
from flask_restful import reqparse
from flask_restful import Resource


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('avatar',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def get(self, username):
        user = self.find_by_username(username)
        if user:
            return user
        return {'message': 'User not exist.'}, 404


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with name '{}' already exists.".format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO users (user_id, username, password, email, avatar, status) \
                 VALUES (null, ?, ?, ?, ?, ?)"""

        cursor.execute(query, (data['username'],
                               data['password'],
                               data['email'],
                               data['avatar'],
                               data['status']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM channels'
        result = cursor.execute(query)
        row = result.fetchall()
        connection.close()

        if row:
            return {'channels': row}
        return {'message': 'Channels not exists.'}, 404
