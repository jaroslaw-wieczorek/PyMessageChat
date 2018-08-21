import sys
import sqlite3
from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt import jwt_required
from models.channel import ChannelModel


class ResourceChannel(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be blank')
    
    # @jwt_required()
    def get(self, name):
        channel = self.find_by_name(name)
        if channel:
            return channel
        return {'message': 'Channel not found'}, 404

    def post(self):
        data = ResourceChannel.parser.parse_args()

        if ChannelModel.find_by_name(data['name']):
            return {'message': "An channel with name '{}' already exists.".format(data['name'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO channels (channel_id, name) \
                 VALUES(null, ?)"""
        cursor.execute(query, (data['name'], ))
        connection.commit()
        connection.close()

        return {"message": "Channel created successfully."}, 201

    def delete(self):
        data = ResourceChannel.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print("looking for id of channel by name")
        result = ChannelModel.fing_id_by_name(data['name'])
        print(result, file=sys.stderr)
        if result["channel_id"] is None:
            print("Inside")
            return { 'message': 'Channel not exist!'}, 400

        print(result, file=sys.stderr)
        query = "DELETE FROM messages WHERE channel_id=?"
        cursor.execute(query, (result['channel_id'],))

        query = "DELETE FROM channels WHERE name=?"
        cursor.execute(query, (data['name'],))

        connection.commit()
        connection.close()

        return { 'message': 'Channel deleted'}, 201


"""

    def put(self, name):
        data = Channel.parser.parse_args()
        item = next(filter(lambda x: x['name'] != name, items), None)
        if item is None:
            item = {'name': data['name']}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
"""

class ChannelList(Resource):
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
