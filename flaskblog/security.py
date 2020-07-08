from flaskblog import db, bcrypt
from flaskblog.models import User


def authenticate(username, password):
    user = User.query.filter_by(username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.filter_by(user_id)