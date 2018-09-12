import sqlite3
from db import db
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String(64), unique=True,
                   primary_key=True, nullable=False)

    email = db.Column(db.String(64), unique=True, nullable=False)

    username = db.Column(db.String(64), unique=True, nullable=False)

    password = db.Column(db.String(64), nullable=False)

    avatar = db.Column(db.String(64), nullable=False)

    status = db.Column(db.String(3))

    def __init__(self, _id, username, password, email, avatar, status):
        # used _id because id is python keyword than self.id.
        self.id = _id
        self.email = email
        self.username = username
        self.password = password
        self.avatar = avatar
        self.status = status

        

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)