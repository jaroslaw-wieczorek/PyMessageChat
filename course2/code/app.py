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

#from security import authenticate
#from security import identity as identity_function

from resources.user import User
from resources.user import UserLogin
from resources.user import UserRegister
from resources.user import UserList

from resources.message import Message
from resources.message import MessageList

from resources.channel import Channel
from resources.channel import ChannelList

from datetime import timedelta



# nadanie nazwy pliku
app = Flask(__name__)
app.secret_key = 'josie'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


app.config['JSON_AS_ASCII'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


#@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'),
                    'username': identity.username
                    })


# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
# pp.config['JWT_AUTH_USERNAME_KEY'] = 'email'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')

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
    app.run(port=5000, debug=True)

