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
                        required=False,
                        help='This field cannot be blank')

    @jwt_required()
    def get(self, name):
        channel = ChannelModel.find_by_name(name)
        if channel:
            return channel.json()
        return {'message': 'Channel not found'}, 404

    def post(self, name):
        if ChannelModel.find_by_name(name):
            return {'message': "An channel with name '{}' already exists.".format(name)}, 400

        #try:
        #    data = ResourceChannel.parser.parse_args()
        #except:
        #    channel = ChannelModel(name, data['id'])

        channel = ChannelModel(None, name)

        try:
            channel.insert()
        except Exception as err:
            return {'message': 'An error occured inserting the item\n', 'error': err.message}, 500
        return channel.json(), 201

    def put(self, name):
        data = ResourceChannel.parser.parse_args()

        channel = ChannelModel.find_by_name(name)
        item_id = ChannelModel.find_id_by_name(name)

        update_channel = ChannelModel(item_id['channel_id'], data['name'])

        # update_channel will be used to updated users in channels
        if channel is None:
            try:
                update_channel.insert()
            except: 
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                update_channel.update()
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        return update_channel.json()

   
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = ChannelModel.find_id_by_name(name)
        print("RESULT:", result)
        if result["channel_id"] is None:
            return {'message': 'Channel not exist!'}, 400

        query = "DELETE FROM messages WHERE channel_id=?"
        cursor.execute(query, (result['channel_id'],))

        query = "DELETE FROM channels WHERE channel_id=?"
        cursor.execute(query, (result['channel_id'],))

        connection.commit()
        connection.close()

        return {'message': 'Channel deleted'}, 201


class ChannelList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM channels'
        result = cursor.execute(query)

        channels = []

        for row in result:
            channels.append({'channel_id': row[0], 'name': row[1]})
        connection.close()

        return {'channels': channels}, 200
