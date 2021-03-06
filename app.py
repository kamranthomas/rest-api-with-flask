import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # important to mention debug=True