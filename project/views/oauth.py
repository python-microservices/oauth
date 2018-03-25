from flask_bcrypt import Bcrypt
from flask_jwt import JWT

from project.models.models import User

bcrypt = Bcrypt()


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(
            user.password, password
    ):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


jwt = JWT(authentication_handler=authenticate, identity_handler=identity)
