# Reprezentation of user
import sys
import sqlite3

from models.user import UserModel
from flask_restful import reqparse
from flask_restful import Resource

from hashes import randomData
from hashes import hashData


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
            return {"message": "A user with that name already exists."}, 400

        #trash = security.randomRubbish()
        #other_data = ''.join(data['username'])
        #other_data.join(data['email'])
        #user_id = security.hashRubbish(_data=other_data)

        _id = security.randomRubbish()
        user = UserModel(_id, **data)

        user.save_to_db()

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
