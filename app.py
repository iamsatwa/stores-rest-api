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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"  # database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth end point


@app.before_first_request  # Registers a function to be run before the first request to this instance of the application
def create_tables():
    db.create_all()        # if data.db is not created then it will create data.db before the first request


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(Users, '/users')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)