from flask_restful import abort
from functools import wraps
from flask_jwt import JWT, current_identity
from hashlib import md5
from models import Client
import system.app
import config.app

system.app.config['SECRET_KEY'] = config.app.secret_key

def __get_user(username, password):
    password_hash = md5(password.encode('utf-8')).hexdigest()
    client = Client.query.filter_by(username=username).first()
    if client and client.password == password:
        return client

def __identity(payload):
    id = payload['identity']
    return Client.query.filter_by(id=id).first()

jwt = JWT(system.app, __get_user, __identity)

def __authentication():
    return Client.query.filter_by(username=current_identity.username).first() is not None

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        
        acct = __authentication()

        if acct:
            return func(*args, **kwargs)
        
        abort(401)
    
    return wrapper