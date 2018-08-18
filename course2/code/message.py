import sqlite3
from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt import jwt_required


class Message(Resource):
    def __init__(self, _id, _channel_id, content, time, user_id):
        # used _id because id is python keyword than self.id.
        self.id = _id
        self.content = content
        self.time = time
        self.channel_id = _channel_id
        self.user_id = user_id


class MessageList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="Message can't be empty"
                        )

    @jwt_required()
    def get(self, channel_id, message_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM messages WHERE channel_id=? and message_id=;"""

        result = cursor.execute(query, (channel_id, message_id))
        row = result.fetchone()
        connection.close()

        if row:
            return {'message': {
                    'channel_id': row[0],
                    'message_id': row[1],
                    'content': row[2],
                    'user_id': row[3],
                    'time': row[4],
                    }}

        return {'message': "Not found msg with id '{}'.".format(msg_id)}, 404

    @jwt_required()
    def post(self, message_id):
        if next(filter(lambda x: x['message_id'] == message_id, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = """SELECT * FROM messages WHERE id=?"""

        result = cursor.execute(query, (message_id, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'message': {
                    'channel_id': row[0],
                    'message_id': row[1],
                    'content': row[2],
                    'user_id': row[3],
                    'time': row[4],
                    }}

        return {'message': "An message with id '{}' not exists.".format(message_id)}, 404