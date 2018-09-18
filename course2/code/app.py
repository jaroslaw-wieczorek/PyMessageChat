from flask import Flask
from flask import jsonify
from flask import render_template

#from flask.ext.hashing import Hashing
from flask_restful import Api
from flask_restful import Resource


from flask_jwt_extended import JWTManager

from flask_jwt import jwt_required

from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required

from blacklist import BLACKLIST

#from security import authenticate
#from security import identity as identity_function

from resources.user import User
from resources.user import UserList
from resources.user import UserLogin
from resources.user import UserRegister
from resources.user import TokenRefresh

from resources.message import Message
from resources.message import MessageList

from resources.channel import Channel
from resources.channel import ChannelList

from datetime import timedelta

# nadanie nazwy pliku
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['JSON_AS_ASCII'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
app.secret_key = 'josie'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(ChannelList, '/channels')
api.add_resource(Channel, '/channels/<string:name>')

api.add_resource(MessageList, '/channels/<string:channel_name>/messages')
api.add_resource(Message, '/channels/<string:channel_name>/messages/<string:message_id>')


@app.route('/')
def home():
    return render_template('chat.html')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=False)

