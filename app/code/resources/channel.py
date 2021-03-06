import sys
import json
import sqlite3

from datetime import date
from datetime import datetime
from datetime import timezone

from hashes import randomData
from hashes import hashData

from flask import Flask
from flask import jsonify

from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_jwt_extended import get_jwt_identity

from models.user import UserModel
from models.channel import ChannelModel
from models.message import MessageModel


class Channel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help='This field cannot be blank')

    parser.add_argument('users',
                        type=str,
                        required=False,
                        action='append',
                        help='This field cannot be blank')

    parser.add_argument('owners',
                        type=str,
                        required=False,
                        action='append',
                        help='This field cannot be blank')

    @jwt_required
    def get(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel:
            return channel.json()
        return {'message': 'Channel not found'}, 404

    @jwt_required
    def post(self, name):
        check = ChannelModel.find_by_name(name)
        if check:
            return {'message': "An channel with that name already exists."}, 400

        data = Channel.parser.parse_args()

        random_data = randomData()

        timestamp = datetime.utcnow().timestamp()

        channel_id = hashData(random_data, str(timestamp) + str(name))

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        owner = user.username

        owners = set()
        owners.add(owner)

        for item in data["owners"]:
            owners.add(item)

        print(owners)

        users = set()
        users.add(owner)
        for item in data["users"]:
            users.add(item)
        print(users)

        try:
            owners.remove('')
        except Exception as err:
            pass

        try:
            users.remove('')
        except Exception as err:
            pass

        # None is used because the user will not set the channel id.
        try:
            channel = ChannelModel(channel_id, str(name),
                                   json.dumps(list(owners)),
                                   json.dumps(list(users))
                                   )
            channel.save_to_db()
            channel.save_to_db()

        except Exception as err:
            return {'message': 'An error occured inserting the item\n',
                    'error': err}, 500

        return channel.json(), 201

    @jwt_required
    def put(self, name):
        channel = ChannelModel.find_by_name(name)
        data = Channel.parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if channel is None:
            timestamp = datetime.utcnow().timestamp()
            random_data = randomData()

            channel_id = hashData(random_data, str(timestamp) + str(name))

            owner = user.username
            owners = set()
            owners.add(owner)

            if data["owners"] and hasattr(data["owners"], '__iter__'):
                for item in data["owners"]:
                    owners.add(item)

            users = set()
            users.add(owner)

            if data["users"] and hasattr(data["users"], '__iter__'):
                for item in data["users"]:
                    users.add(item)

            print(owners, users)

            try:
                owners.remove('')
                owners.remove('null')
            except Exception as err:
                pass

            try:
                users.remove('')
                users.remove('null')
            except Exception as err:
                pass

            channel = ChannelModel(channel_id, name,
                                   json.dumps(list(owners)),
                                   json.dumps(list(users))
                                   )

        elif (not ChannelModel.find_by_name(data['name']) or
              data['name'] == name):

            if user.username not in channel.owners:
                return {
                    'message': 'You arn\'t owner channel: ' + channel.name
                }
            owner = user.username
            owners = set()
            owners.add(owner)
            if data["owners"] and hasattr(data["owners"], '__iter__'):
                for item in data["owners"]:
                    owners.add(item)

            users = set()
            users.add(owner)
            if data["users"] and hasattr(data["users"], '__iter__'):
                for item in data["users"]:
                    users.add(item)

            try:
                owners.remove('')
            except Exception as err:
                pass

            try:
                users.remove('')
            except Exception as err:
                pass

            channel.owners = json.dumps(list(owners))
            channel.users = json.dumps(list(users))

        else:
            return {'message': "An channel with name '{}' already exists".format(data['name'])}, 404
        channel.save_to_db()
        return channel.json(), 201

    @jwt_required
    def delete(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel is not None:
            messages = MessageModel.find_msgs_by_channel_id(channel.channel_id)
            if messages is not None:
                for message in messages:
                    message.delete_from_db()
            channel.delete_from_db()
            return {'message': 'Channel deleted'}, 201
        return {'message': "An channel not found"}, 404


class UserChannelList(Resource):
    @fresh_jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user:
            name = user.username
            channels = ChannelModel.find_channels_by_username(name)
            channel_list = []

            for channel in channels:
                if (name in json.loads(channel.owners) or
                   name in json.loads(channel.users)):
                        channel_list.append(channel.json())

            if channel_list:
                return {'channels': channel_list}, 200
            else:
                return {'message': 'User hasn\'t got any channel'}, 200
        return {'message': 'Channels not found'}, 404


class CheckIsChannelOwner(Resource):
    @jwt_required
    def get(self, channel_name):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        channel = ChannelModel.find_by_name(channel_name)
        if channel:
            if user.username in channel.owners:
                return {'is_owner': True}, 200
            return {'is_owner': False}, 403
        return {'message': 'Channel not found'}, 404


class ChannelList(Resource):
    @fresh_jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user:
            name = user.username
            user_channels = ChannelModel.find_channels_by_user(name)
            owner_channels = ChannelModel.find_channels_by_owner(name)

            channel_list = []

            for channel in owner_channels:
                if name in json.loads(channel.owners):
                        channel_list.append(channel.json())

            for channel in user_channels:
                if name in json.loads(channel.users) and(
                    channel.json() not in channel_list
                ):
                    channel_list.append(channel.json())

            if channel_list:
                return {'channels': channel_list}, 200
            else:
                return {'message': 'User hasn\'t got any channel'}, 200
        return {'message': 'Channels not found'}, 404
