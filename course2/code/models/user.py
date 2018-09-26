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

    avatar = db.Column(db.Text, nullable=False)

    status = db.Column(db.Boolean, default=False)

    def __init__(self, _id, username, password, email, avatar, status=False):
        # used _id because id is python keyword than self.id.
        self.id = _id
        self.email = email
        self.username = username
        self.password = password
        self.avatar = avatar
        self.status = status

    def json(self):
        return {
            'username': self.username,
            'avatar': self.avatar,
            'status': self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    '''
    def is_active(self):
        return True

    def is_anonymous(self):
        return False


    def is_authenticated(self):
        return self.authenticated
    '''

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_avatar(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user.avatar
        else:
            return None

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
