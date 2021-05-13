from models.user import UserModel
from passlib.hash import sha256_crypt


def authenticate(username, password):
    user = UserModel.find_user_name(username)
    if user and sha256_crypt.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_id(user_id)