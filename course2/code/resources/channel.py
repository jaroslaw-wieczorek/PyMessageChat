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
                        type=str,
                        required=True,
                        action='append',
                        help='This field cannot be blank')

    parser.add_argument('owners',
                        type=str,
                        required=True,
                        action='append',
                        help='This field cannot be blank')

    #@jwt_required()
    def get(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel:
            return channel.json()
        return {'message': 'Channel not found'}, 404

    def post(self, name):
        check = ChannelModel.find_by_name(name)
        if check:
            return {'message': "An channel with name '{}' already exists.".format(name)}, 400

        data = ResourceChannel.parser.parse_args()
        channel = ChannelModel(None, str(name), json.dumps(data["owners"]), json.dumps(data["users"]))
        try:
            channel.save_to_db()

        except Exception as err:
            return {'message': 'An error occured inserting the item\n', 'error': err}, 500
        return channel.json(), 201

    def put(self, name):
        channel = ChannelModel.find_by_name(name)
        data = ResourceChannel.parser.parse_args()
        print(data)
        # update_channel will be used to updated users in channels
        if channel is None:
            channel = ChannelModel(None, name, json.dumps(data['owners']),  json.dumps(data['users']))
        else:
            channel.name = data['name']
            channel.owners = json.dumps(data['owners'])
            channel.users = json.dumps(data['users'])

        channel.save_to_db()
        return channel.json(), 201

    def delete(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel:
            channel.delete_from_db()
            return {'message': 'Channel deleted'}, 201
        return {'message': "An channel with name '{}' already not exists".format(name)}, 404


class ChannelList(Resource):
    def get(self):

        channels = ChannelModel.query.all()
        
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM channels'
        result = cursor.execute(query)

        channels = []

        for row in result:
            channels.append({'channel_id': row[0], 'name': row[1], 'owners': json.loads(row[2]), 'users': json.loads(row[3])})
        connection.close()
        """
        channel_list = []
        for channel in channels:
            channel_list.append(channel.json())
        return {'channels': channel_list}, 200
