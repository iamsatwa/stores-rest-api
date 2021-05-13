import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from passlib.hash import sha256_crypt


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot blank")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_user_name(data['username']):
            return {"message": "user - {} is present in DB".format(data['username'])}, 400
        user = UserModel(data['username'], sha256_crypt.encrypt(data['password']))
        user.save_to_db()
        return {"message": "user - {} created successfully".format(data['username'])}, 201


class Users(Resource):
    def get(self):
        user_list= []
        users = UserModel.get_all_users()
        for rec in users:
            user = {"username": rec.username, "password":rec.password}
            user_list.append(user)

        return {"users": user_list}