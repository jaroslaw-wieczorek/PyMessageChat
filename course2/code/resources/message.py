import sys
import sqlite3
from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt import jwt_required

from datetime import datetime
from models.message import MessageModel
from models.channel import ChannelModel


class ResourceMessage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help='This field cannot be blank')

    parser.add_argument('time',
                        type=str,
                        required=True,
                        help='This field cannot be blank')

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank')

    parser.add_argument('avatar',
                        type=str,
                        required=True,
                        help='This filed cannot be blank')


    #@jwt_required()
    def get(self, channel_name, message_id):
        data = ChannelModel.find_id_by_name(channel_name)
        print(data)
        message = MessageModel.find_by_channel_id_and_message_id(data["channel_id"], message_id)

        print(message)
        if message:
            return message.json(), 202
        return {'message': 'Message not found'}, 404

    def post(self, channel_name):
        data = ResourceMessage.parser.parse_args()

        channel_info = ChannelModel.find_id_by_name(channel_name)
        if channel_info:
            return {"message": "Channel not exist."}, 404
        print(channel_info)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(channel_info)

        query = """INSERT INTO messages (message_id, channel_id, content, time, username, avatar) VALUES (null, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (channel_info['channel_id'],
                               data['content'],
                               data['time'],
                               data['user_id'],
                               data['avatar'])
                       )

        connection.commit()
        connection.close()

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
        data = ChannelModel.find_id_by_name(channel_name)
        print(data)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM messages WHERE channel_id=?'
        result = cursor.execute(query, (data['channel_id'],))
        rows = result.fetchall()
        connection.close()

        messages = []
        if rows:
            for row in rows:
                messages.append(MessageModel(*row).json())
            return {"messages": messages}
        return {'message': 'Messages or channel not exists.'}, 404

