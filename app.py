from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from api_v4.security import authenticate, identity
from api_v4.resources.items import Item, ItemList
from api_v4.resources.users import UserRegister
from api_v4.db import db

app = Flask(__name__)
api = Api(app)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data.db'
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
