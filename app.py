import os
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, Users
from resources.items import Item, ItemList
from resources.stores import Store, StoreList
# JWT - json web token
app = Flask(__name__)
app.secret_key ='satyajit'
# read the DATABASE_URL from Heroku. If it is not available then it will take sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600) # config JWT to expire within  an hour
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth end point


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(Users, '/users')

# if __name__ == "__main__":
#     from db import db
#     db.init_app(app)
#
#     app.run(port=5000, debug=True)
