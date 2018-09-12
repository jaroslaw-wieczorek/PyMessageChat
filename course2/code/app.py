from flask import Flask
from flask import jsonify
from flask import render_template

#from flask.ext.hashing import Hashing
from flask_restful import Api
from flask_restful import Resource


from flask_jwt import JWT

from flask_jwt import jwt_required

from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required


from security import authenticate
from security import identity as identity_function

from models.message import MessageModel

from resources.user import UserList, UserRegister
from resources.message import MessageList, ResourceMessage
from resources.channel import ChannelList, ResourceChannel

from datetime import timedelta

# nadanie nazwy pliku
app = Flask(__name__)
app.secret_key = 'josie'
api = Api(app)

app.config['JSON_AS_ASCII'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'),
                    'username': identity.username
                   })

#api.add_resource(Item, '/item/<string:name>')
#api.add_resource(ItemList, '/items')

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')


api.add_resource(ChannelList, '/channels')
api.add_resource(ResourceChannel, '/channels/<string:name>')

api.add_resource(MessageList, '/channels/<string:channel_name>/messages')
api.add_resource(ResourceMessage, '/channels/<string:channel_name>/message')

#api.add_resource(ResourceMessage, '/channel/<string:channel_name>/<int:message_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

"""
# Store app
# POST /store data: {name:}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    # this allow get data back in reqest
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store<string:name> # 'http://127.0.0.1:5000/store/name'
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

    # iterate over stores
    # if store name matches, return it
    # if none match, return an error message


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string : name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})

"""