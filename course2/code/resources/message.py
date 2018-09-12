import sys
import sqlite3
import json


from hashes import randomData
from hashes import hashData


from flask import Flask
from flask import jsonify

#from flask.ext.hashing import Hashing

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt import jwt_required

from datetime import datetime
from models.user import UserModel
from models.message import MessageModel
from models.channel import ChannelModel
from resources.channel import ResourceChannel

from werkzeug.security import generate_password_hash, check_password_hash

class ResourceMessage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('message_id',
                        type=str,
                        required=False,
                        help='This field cannot be blank')
   # parser.add_argument('time',
   #                     type=str,
   #                     required=False,
   #                     help='This field cannot be blank')

    parser.add_argument('username',
                        type=str,
                        required=False,
                        help='This field cannot be blank')


    # @jwt_required()
    def get(self, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            data = ResourceMessage.parser.parse_args()

            if hasattr(data, 'message_id'):
                message = MessageModel.find_msg_by_id_and_channel_id(
                    data['message_id']
                )
            else:
                return {'message': 'Bad request - need message id'}, 404

            if message:
                return message.json(), 202
        else:
            return {'message': 'Channel not found'}, 404
        return {'message': 'Message not found'}, 404

    def post(self, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            data = ResourceMessage.parser.parse_args()

            date_now = datetime.utcnow()
            timestamp = date_now.timestamp()
            random_data = randomData()

            message_id = hashData(random_data, str(timestamp) + str(channel_name))

            #try:
            message = MessageModel(message_id, channel_id,
                                   data["content"], date_now,
                                   data["username"], "place for avatar")
            message.save_to_db()
           #except Exception as err:
           #     return {'message': 'internall error ' + str(err)}, 500
        else:
            return {'message': 'Channel not exist.'}, 404

        return {"message": "Message created successfully."}, 201

    def delete(self, channel_name):
        channel_id = ChannelModel.find_by_name(channel_name)
        if channel_id:
            data = ResourceMessage.parser.parse_args()

            if hasattr(data, 'message_id'):
                message = MessageModel.find_msg_by_id_and_channel_id(
                    channel_id.channel_id, data['message_id'])

                if message:
                    message.delete_from_db()
                    return {'message': 'Message was deleted.'}, 201
                else:
                    return {'message': 'Not found message with that id'}, 404
            else:
                return {'message': 'Bad request - need message id'}, 400
        else:
            return {'message': 'Not found channel with that name'}, 404


class MessageList(Resource):
    def get(self, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            messages_list = []
            messages = MessageModel.find_msgs_by_channel_id(channel_id)
            if messages:
                for message in messages:
                    messages_list.append(message.json())
                return {"messages": messages_list}
            else:
                return {'message': 'Channel is empty.'}, 200
        else:
            return {'message': 'Channel doesn\'t exist.'}, 200
