from db import db
import json

class ChannelModel(db.Model):

    __tablename__ = 'channels'

    channel_id = db.Column(db.String(64), primary_key=True, unique=True)
    name = db.Column(db.String(64), unique=True)
    owners = db.Column(db.Text)
    users = db.Column(db.Text)

    messages = db.relationship('MessageModel')

    def __init__(self, _channel_id, name, owners, users):
        self.channel_id = _channel_id
        self.name = name
        self.owners = owners
        self.users = users

    def json(self):
        return {
            'channel_id': self.channel_id,
            'name': self.name,
            'owners': json.loads(self.owners),
            'users': json.loads(self.users),
            'messages': [message.json() for message in self.messages]
        }

    @classmethod
    def find_channels_by_username(cls, username):
        return cls.query.filter(ChannelModel.owners.contains(username)).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # SELECT * FROM items WHERE name=name

    @classmethod
    def find_id_by_name(cls, name):
        channel = cls.query.filter_by(name=name).first()
        if channel:
            return channel.channel_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(channel_id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
