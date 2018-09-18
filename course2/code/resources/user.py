# Reprezentation of user
import sys
import sqlite3

from hashes import hashData
from hashes import randomData

from models.user import UserModel
from blacklist import BLACKLIST

from flask_restful import reqparse
from flask_restful import Resource

from werkzeug.security import safe_str_cmp

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank")

_user_parser.add_argument('email',
                          type=str,
                          required=False,
                          help="This field cannot be blank")

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank")

_user_parser.add_argument('avatar',
                          type=str,
                          required=False,
                          help="This field cannot be blank")

_user_parser.add_argument('status',
                          type=bool,
                          required=False,
                          default=False,
                          help="Status is setup by server")


class UserRegister(Resource):

    def get(self, username):
        user = self.find_by_username(username)
        if user:
            return user.json()
        return {'message': 'User not exist.'}, 404

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that name already exists."}, 400

        elif UserModel.find_by_email(data['email']):
            return {"message": "That email is in use."}, 400

        random_data = randomData()
        #print(random_data)
        _id = hashData(str(random_data))
        #print(_id)
        user = UserModel(_id, **data)

        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        users = UserModel.query.all()

        if users:
            return {'users': [user.json() for user in users]}
        return {'message': 'Users not exists.'}, 404


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identyfier for a JWT
        BLACKLIST.add(jti)
        return {'messages': 'Succesfuly logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
