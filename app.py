from datetime import timedelta
import os
from os.path import join, dirname
import bcrypt
from dotenv import load_dotenv
from flask_graphql_auth.main import GraphQLAuth
from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from flask_cors import CORS, cross_origin


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Flask app configuration
app = Flask(__name__)
configEnv = os.environ.get('CONFIG_ENV')

jwt_secret_key = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = jwt_secret_key

app.config.from_object(configEnv)

cors = CORS(app)
auth = GraphQLAuth(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

@app.route("/graphql", methods=["GET", "POST"])
@cross_origin()
def graphql_playground():
    pass

if __name__ == '__main__':
    init_db()
    app.run(debug=True,host=os.environ.get('HOST'), port=os.environ.get('PORT'))
