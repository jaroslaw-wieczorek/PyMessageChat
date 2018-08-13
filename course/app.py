from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template


from flask_restful import Api
from flask_restful import Resource


from flask_jwt import JWT
from flask_jwt import jwt_required

from security import authenticate, identity


# nadanie nazwy pliku
app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)


users=[] 


class User(Resource):
    def get(self, name):
        """
            filter function return filter object with filtered data used lambda
            when we use next on filter object we get a first item, when we use next many time 
            we get next values from filter object. Next can raise error
        """

        user = next(filter(lambda x: x['name'] == name, users), None)
        return {'user': user}, 200 if user is not None else 404


    def post(self, name):
        if (filter(lambda x: x['name'] == name, users), None) is not None:
            return {'message': "An user with name '{}' already exists.".format(name)}, 400
        
        data = request.get_json() # never use arg force=True

        user = {'name': user, 'avatar': data['avatar']}
        users.append(user)
        return user, 201


class UserList(Resource):
    def get(self):
        return {'users': users}, 200



api.add_resource(User, '/user/<string:name>')
api.add_resource(UserList, '/users')

'''JWT How it work?
JWT create a new endpoint that endpoit is /auth.
when we call /auth we send it a username and a password
and the JWT extension gets that username and password
and sends it over to the authenticate functions.
That takes in a username and password.

We are then going to find the corect a user object
using that username and we're going to compare its password
to the one that we received thorught the auth endpoint.


If they match we're going to return the user and that becomes sort of the
identity.

So what happens nest is the auth endpoint.

'''

# jwt = JWT(app, authenticate, identity)


stores = [
    {
        'name': 'Jack',
        'users': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]
# POST - used to recive data
# GET - used to send data back only



# Store app
# POST /store data: {name:}
@app.route('/')
def home():
    return render_template('index.html')
"""
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
app.run(port=5000)
