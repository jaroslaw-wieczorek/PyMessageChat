import sys
import sqlite3
import json

from hashes import randomData
from hashes import hashData

from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt_extended import jwt_optional
from flask_jwt_extended import jwt_required

from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required

from datetime import datetime
from models.user import UserModel
from models.message import MessageModel
from models.channel import ChannelModel

from resources.channel import Channel

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class Message(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('message_id',
                        type=str,
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('username',
                        type=str,
                        required=False,
                        help='This field cannot be blank')
    """
    @jwt_required
    def get(self, channel_name, message_id):
        channel_id = ChannelModel.find_id_by_name(channel_name)

        if channel_id:
            message = MessageModel.find_msg_by_channel_id_msg_id(
                channel_id, message_id)

            if message:
                return message.json(), 202
            else:
                return {'message': 'Message not found'}, 404
        else:
            return {'message': 'Channel not found'}, 404
    """
    @jwt_required
    def post(self, channel_name):

        channel_id = ChannelModel.find_id_by_name(channel_name)

        if channel_id:
            random_data = randomData()
            message_id = hashData(str(random_data))

            if MessageModel.find_msg_by_channel_id_msg_id(channel_id,
                                                          message_id):
                return {'message': 'Bad message id'}, 400

            data = Message.parser.parse_args()
            date_now = datetime.utcnow()

            user_id = get_jwt_identity()
            user = UserModel.find_by_id(user_id)

            message = MessageModel(message_id, channel_id,
                                   data["content"], date_now,
                                   user.username,
                                   UserModel.get_avatar(user.username))

            message.save_to_db()
            return message.json(), 201
        else:

            return {'message': 'Channel not exist.'}, 404

    @jwt_required
    def delete(self, channel_name, message_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            message = MessageModel.find_msg_by_channel_id_msg_id(
                channel_id, message_id)

            if message:
                message.delete_from_db()
                return {'message': 'Message was deleted.'}, 201
            else:
                return {'message': 'Message not found.'}, 404


class MessageList(Resource):
    @jwt_optional
    def get(self, channel_name):
        user_id = get_jwt_identity()

        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            messages_list = [message.json() for message in
                             MessageModel.query.filter_by(
                             channel_id=channel_id).all()]

            if user_id:
                return {"messages": messages_list}, 200
            else:
                return {"messages": "Not available for non-logged users."}, 403
        else:
            return {'message': 'Channel with that name not found.'}, 404
