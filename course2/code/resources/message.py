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
                        type=datetime,
                        required=True,
                        help='This field cannot be blank')

    parser.add_argument('channel_id',
                        type=int,
                        required=True,
                        help='This field cannot be blank')

    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help='This field cannot be blank')


    # @jwt_required()
    def get(self, message_id):
        message = self.find_by_id(message_id)
        if message:
            return message
        return {'message': 'Message not found'}, 404

    def post(self):
        data = ResourceMessage.parser.parse_args()

        if Message.find_by_id(data['message_id']):
            return {'message': "An message with id '{}' already exists.".format(data['id'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO messages (message_id, contents, time, channel_id, user_id) VALUES (null, ?, ?, ?, ?)"""
        cursor.execute(query, (data['content'],
                               data['time'],
                               data['channel_id'],
                               data['user_id']))
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

        return { 'message', 'Item deleted'}, 201


class MessageList(Resource):
    def get(self, channel_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM messages WHERE channel_id=?'
        result = cursor.execute(query, (channel_id,))
        rows = result.fetchall()
        connection.close()

        if rows:
            return {'messages': rows}
        return {'message': 'Channels not exists.'}, 404
