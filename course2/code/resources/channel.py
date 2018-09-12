import sys
import json
import sqlite3

from security import randomRubbish
from security import hashRubbish

from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt import jwt_required
from models.channel import ChannelModel
from models.message import MessageModel


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

        trash = randomRubbish()
        print("TRASH:", trash)
        channel_id = hashRubbish(trash)
        print("HASH:", channel_id)
        print("LEN:", len(channel_id))
        print("TYPE:", type(channel_id))

        # None is used because the user will not set the channel id.
        channel = ChannelModel(str(channel_id), str(name),
                               json.dumps(data["owners"]),
                               json.dumps(data["users"])
                               )
        try:
            channel.save_to_db()

        except Exception as err:
            return {'message': 'An error occured inserting the item\n',
                    'error': err}, 500


        return channel.json(), 201

    def put(self, name):
        channel = ChannelModel.find_by_name(name)
        data = ResourceChannel.parser.parse_args()

        if channel is None:
            trash = randomRubbish()
            print("TRASH:", trash)
            channel_id = hashRubbish(trash)
            print("HASH:", channel_id)
            print("LEN:", len(channel_id))
            print("TYPE:", type(channel_id))

            channel = ChannelModel(channel_id, name,
                                   json.dumps(data['owners']),
                                   json.dumps(data['users'])
                                   )

        elif not ChannelModel.find_by_name(data['name']) or data['name'] == name:
            channel.name = data['name']
            channel.owners = json.dumps(data['owners'])
            channel.users = json.dumps(data['users'])
        else:
            return {'message': "An channel with name '{}' already exists".format(data['name'])}, 404
        channel.save_to_db()
        return channel.json(), 201

    def delete(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel is not None:
            messages = MessageModel.find_msgs_by_channel_id(channel.channel_id)
            if messages is not None:
                for message in messages:
                    message.delete_from_db()
            channel.delete_from_db()
            return {'message': 'Channel deleted'}, 201
        return {'message': "An channel with name '{}' already not exists".format(name)}, 404


class ChannelList(Resource):
    def get(self):
        channels = ChannelModel.query.all()
        channel_list = []
        print("CHANNELS: ", channels)
        if channels != [None]:
            for channel in channels:
                print("CHANNEL: ", channel)
                channel_list.append(channel.json())
            return {'channels': channel_list}, 200
        return {'message': 'Channels not exists'}
