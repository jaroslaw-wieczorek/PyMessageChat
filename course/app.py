from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT. jwt_required

from security import authenticate, identity

# nadanie nazwy pliku
app = Flask(__name__)
app.secret_key = 'jose'

""" How it work?
JWT create a new endpoint that endpoit is /auth.
when we call /auth we send it a username and a password
and the JWT extension gets that username and password
and sends it over to the authenticate functions.
That takes in a username and password.

We are then going to find the corect a user object
using that username and we're going to compare its password
to the one that we received thorught the auth endpoint.


If they match we're going to return the user and that becomes sort of the identity.

So what happens nest is the auth endpoint.
2

"""

jwt = JWT(app, authenticate, identity)

@jwt_required()


store = [
    {
        'name':'My Wonderful Store',
        'items' : [
            {
                'name':'My Item',
                'price' : 15.99
            }
        ]
    }


]

# POST - used to recive data
# GET - used to send data back only

# Store app

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    pass

# GET /store<string:name> # 'http://127.0.0.1:5000/store/name'
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    pass


# GET /store
@app.route('/store', methods=['GET'])
def get_store(name):
    pass

# POST /store/<string : name>/item {name:, price:}
@app.route('/store/<string:name/item', methods=['POST'])
def create_item_in_store(name):
    pass

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def get_items_in_store(name):
    pass



app.run(port=5000)
