from db import db
import json
from datetime import datetime
from datetime import timedelta
from json_encoder import DateEncoder
from models.channel import ChannelModel


class MessageModel(db.Model):

    __tablename__ = "messages"

    message_id = db.Column(db.String(64), primary_key=True,
                           unique=True,
                           nullable=False)

    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #channel = db.relationship('ChannelModel', backref='channels')
    channel_id = db.Column(db.String(64), nullable=False)#, db.ForeignKey('channels.channel_id'))
    username = db.Column(db.String(64), nullable=False)
    avatar = db.Column(db.Text, nullable=False)

    def __init__(self, _message_id, _channel_id, content,
                 time, username, avatar):
        self.message_id = _message_id
        self.channel_id = _channel_id
        self.content = content
        self.time = time
        self.username = username
        self.avatar = avatar

    def json(self):
        return {"message_id": self.message_id,
                "channel_id": self.channel_id,
                "content": self.content,
                "time": json.dumps(str(self.time), cls=DateEncoder),
                "username": self.username,
                "avatar": self.avatar
                }

    @classmethod
    def find_last_msg_by_channel_id(cls, channel_id):
        return cls.query.filter_by(channel_id=channel_id).last()

    @classmethod
    def find_msgs_by_channel_id(cls, channel_id):
        return cls.query.filter_by(channel_id=channel_id).all()

    @classmethod
    def find_msg_by_id_and_channel_id(cls, msg_id, channel_id):
        return cls.query.filter_by(channel_id=channel_id).first()

    @classmethod
    def find_by_channel(cls, channel_name):
        channel_id = ChannelModel.find_id_by_name(channel_name)
        return cls.query.filter_by(channel_id=channel_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
