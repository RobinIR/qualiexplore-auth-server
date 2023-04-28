import os
import bcrypt
from models import Users
from mongoengine import connect

def init_db():
    uri = os.environ.get('DATABASE_URI')
    db = os.environ.get('DATABASE_NAME')
    connect(db=db, host=uri, alias='default')
    users = Users.objects.first()
    users.encrypt_passwords()
