from typing import Dict, Text
from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, IntField, ListField, StringField, BooleanField
)
import bcrypt
import pymongo
from pymongo.encryption import ClientEncryption
from cryptography.fernet import Fernet


class User(EmbeddedDocument):
    username = StringField()
    password = StringField()

    def set_password(self, password):
        """Sets the password hash for the user using bcrypt"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the password hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Users(Document):
    meta = {'collection': 'users'}
    users = ListField(EmbeddedDocumentField(User))
    def encrypt_passwords(self):
        """Encrypts the existing passwords and updates the users collection if it's not encrypted"""
        for user in self.users:
            if user.password and not user.password.startswith('$2b$'):
                user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()

