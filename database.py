import os
from models import Users
from mongoengine import connect

def init_db():
    try:
        uri = os.environ.get('DATABASE_URI')
        db = os.environ.get('DATABASE_NAME')
        connect(db=db, host=uri, alias='default')
        users = Users.objects.first()
        users.encrypt_passwords()
    except Exception as e:
        # Handle the error here
        print(f"An error occurred during database initialization: {e}")
