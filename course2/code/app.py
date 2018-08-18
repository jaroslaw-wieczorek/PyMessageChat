from flask import Flask
from flask import render_template


from flask_restful import Api
from flask_restful import Resource


from flask_jwt import JWT
from flask_jwt import jwt_required

from security import authenticate
from security import identity

from user import UserRegister
from item import Item, ItemList
from message import Message, MessageList
from channell import ChannelList, Channel

# nadanie nazwy pliku
app = Flask(__name__)
app.secret_key = 'josie'
api = Api(app)



jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

api.add_resource(Channel, '/channel/<int:channel_id>')
api.add_resource(ChannelList, '/channels')

api.add_resource(Message, '/channel/<int:channel_id>/<int:message_id>')
api.add_resource(MessageList, '/channel/<int:channel_id>/')
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