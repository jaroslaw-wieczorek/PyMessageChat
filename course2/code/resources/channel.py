import sys
import sqlite3
from flask import Flask
import json
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
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('users',
                        type=list,
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('owners',
                        type=list,
                        required=False,
                        help='This field cannot be blank')

    #@jwt_required()
    def get(self, name):
        channel = ChannelModel.find_by_name(name)
        print(type(channel))
        if channel:
            return channel.json()
        return {'message': 'Channel not found'}, 404

    def post(self, name):
        if ChannelModel.find_by_name(name):
            return {'message': "An channel with name '{}' already exists.".format(name)}, 400

        data = ChannelModel.parser.parse_args()

        channel = ChannelModel(None, name, data["owners"], data["users"])

        try:
            channel.save_to_db()
        except Exception as err:
            return {'message': 'An error occured inserting the item\n', 'error': err.message}, 500
        return channel.json(), 201

    def put(self, name):
        data = ResourceChannel.parser.parse_args()

        channel = ChannelModel.find_by_name(name)

        # update_channel will be used to updated users in channels
        if channel is None:
            channel = ChannelModel(data['name'], data['owners'], data['users'])
        else:
            channel.name = name
            channel.owners = data['owners']
            channel.users = data['users']
        channel.save_to_db()
        return channel.json()

    def delete(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel:
            channel.delete_from_db()
        return {'message': 'Channel deleted'}, 201


class ChannelList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM channels'
        result = cursor.execute(query)

        channels = []

        for row in result:
            channels.append({'channel_id': row[0], 'name': row[1], 'owners': json.loads(row[2]), 'users': json.loads(row[3])})
        connection.close()

        return {'channels': channels}, 200
