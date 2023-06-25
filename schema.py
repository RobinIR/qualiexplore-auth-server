import os
from flask_graphql_auth.decorators import mutation_header_jwt_refresh_token_required, mutation_header_jwt_required, query_header_jwt_required
import graphene
from graphene.types import json
from graphene.types.scalars import String
from graphene_mongo import MongoengineObjectType
from database import init_db
from models import Users as UsersModel, User as UserModel
from dotenv import load_dotenv
import jwt
load_dotenv()

from flask import current_app as app
from flask_graphql_auth import (
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from cryptography.fernet import Fernet

# MongoEngine classes to typecast GraphQL Mutations and Queries for document


class User(MongoengineObjectType):
    class Meta:
        model = UserModel


class Users(MongoengineObjectType):

    class Meta:
        model = UsersModel


# Mutation class for login authentication
# Accepts: Username and Password
# Returns: Auth token and Refresh token
class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username),
        )

# Refresh mutation returns a refreshtoken as string

class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @mutation_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))




class Query(graphene.ObjectType):

    users = graphene.List(Users)
    # Decrypt the username using fernet key. Fernet key is stored in JWT_SECRET_KEY env variable
    def resolve_users(self, info):
        users_list = list(UsersModel.objects.all())
        key = os.getenv('JWT_SECRET_KEY')
        fernet = None
        
        if key is None:
            raise ValueError("Invalid JWT_SECRET_KEY. Key not found or not set.")
        
        try:
            fernet = Fernet(key)
            for users in users_list:
                for user in users.users:
                    try:
                        decrypted_username = fernet.decrypt(user.username.encode('utf-8'))
                        user.username = decrypted_username.decode('utf-8')
                        user.username_decrypted = True
                    except Exception:
                        raise ValueError("Invalid Secret Key To Decrypt Data")
        except Exception as e:
            raise ValueError(f"Error occurred: {str(e)}")
        
        return users_list

# All mutations are implemented as Graphene object type
class MyMutations(graphene.ObjectType):
    login = AuthMutation.Field()
    refresh = RefreshMutation.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
