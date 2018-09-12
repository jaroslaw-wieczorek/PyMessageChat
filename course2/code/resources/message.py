import sys
import sqlite3
import json


from security import randomRubbish
from security import hashRubbish


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
                        required=True,
                        help='This field cannot be blank')

   # parser.add_argument('time',
   #                     type=str,
   #                     required=False,
   #                     help='This field cannot be blank')

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank')


    # @jwt_required()
    def get(self, channel_name, message_id):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
            message = MessageModel.find_msg_by_id_and_channel_id(
                message_id
            )
        if message:
            return message.json(), 202
        return {'message': 'Message not found'}, 404

    def post(self, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        if channel_id:
             data = ResourceMessage.parser.parse_args()

             time = datetime.now()

             message_id="odnfosnfosnfd"

             message = MessageModel(message_id, channel_id, data["content"], json.dumps(time), data["username"], "fdsfsdf")
             message.save_to_db()
        else:
            return {'message': 'First create channel.'}, 404


       





        return {"message": "Message created successfully."}, 201

    def delete(self, channel_name, message_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        channel_id = ChannelModel.get_id_by_name(channel_name)

        query = "DELETE FROM messages WHERE channel_id=? and message_id=?"
        cursor.execute(query, (channel_id, message_id))
        connection.commit()
        connection.close()

        return {'message': 'Item was deleted.'}, 201


class MessageList(Resource):
    def get(self, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        print("Channel id: ", channel_id)
        if channel_id:
            messages_list = []
            messages = MessageModel.find_msgs_by_channel_id(channel_id)
            print("Messages: ", messages)
            if messages:
                for message in messages:
                    messages_list.append(message.json())
                return {"messages": messages_list}
            else:
                return {'message': 'Channel is empty.'}, 200
        else:
            return {'message': 'Channel don\'t exist.'}, 200
