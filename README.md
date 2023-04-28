
# GraphQL server using Flask and MongoDB

This API is built on Flask Python Framework. This server API implements GraphQL query language using Graphene module and connects to MongoDB for storage (Mongoengine). This API authenticates the client access by creating and serving JWT token.

## GraphQl server for Qualiexplore.

This branch is optimized for serving the Qualiexplore application loacted in the following forked GitHub repository. (Mind the branch)

[https://github.com/hrabhijith/qualiexplore/tree/authngql]

## Creation of MongoDb database for Qualiexplore application

This server is used for the user authetication of Qualiexplore application. 

Three MongoDb has encrypted users collection.

1. Install MongoDb database tools in to your PC. [https://www.mongodb.com/try/download/database-tools]
2. Run the following mongoimport command for importing users.json file
`mongoimport --uri <connection_string> --collection <collectionname> --drop --file <filename>`

3. The users collection should be like
```JSON
    {
     "users":[
         {"username":"Encrypted Username","password":"Encrypted Password"},
         {"username":"Encrypted Username","password":"Encrypted Password"}
         ]
    }
```

## Local Installation [only documented for windows]

1. Clone or Download the project in to a directory.

2. Install latest stable version of Python 3. [https://www.python.org/downloads/]

3. Install virtual environment for Python. [https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/]

    * In terminal, type the below command to install virtual environment.

    `py -m pip3 install --user virtualenv`

    * Type the below command in the project directory to create virtual environment.

    `py -m venv env`

    * Type the below command in the project directory to activate the virtual environment.

    `.\env\Scripts\activate`

4. Type the below command in the project directory to install all required modules.

`pip3 install -r requirements.txt`

5. Execute the below command to run the application. (Congifgure variables before this step, see below for more info)

`python3 app.py`

6. The application will start running at 'localhost:5000'.

7. Clients can connect to this server at 'localhost:5000/graphql' using required client modules.


## Installation and Execution using Docker

1. Make sure you have installed Docker. [https://docs.docker.com/get-docker/] 

2. Download the already built image from Docker hub, using the command below.

    `docker pull hrabhijith/gql-mongo:quali`

3. Run the below command in the terminal. (use docker compose with env_vars for this step instead, see below for more info)

    `docker run --name <container_name> -p 5000:5000 hrabhijith/gql-mongo:quali`

4. The application will start running at localhost:<required_port>.


## Configuration variables

Before running the project either the python command in local or docker run in docker container, the environment variables need to be set.


**Local Execution on Windows**

The environment variables will be picked automatically from .env file (included). Refer the below commands for options for the variables.

For Developemnt server

`CONFIG_ENV=config.DevConfig`

For Production Serve (Not Ideal)

`CONFIG_ENV=config.ProdConfig`

Set the secret for JWT token creation

`JWT_SECRET_KEY=yoursecret`

Set the database URI and name

`DATABASE_URI=databaseuri`

`DATABASE_NAME=qualiexplore01`

If needed, set the host name and port number(Default: localhost:5000)

`HOST=hostIP`

`PORT=portnumber`


**Docker container execution**

The docker-compose.yml file is included in the code which helps to set the configuration variables from .env file (which is also included) and runs the docker image in the container. Configure the variable in the .env file accordingly and run the following command.

`docker-compose up`

## GraphQL Playground

Graphene provides an UI to execute the implemented Queries and Mutations in the server, visualize the input and return value types for those queries and mutations. **Also, the same query syntax is used in all consumable client languages.**

The MongoDb collection (Tables/Documents) used for this demo application is shown below.

After the above installation and execution steps, Open a browser and go to 'localhost:5000/graphql'. The UI provides an input field to put quries or mutations, run them and see the results. Below are the inputs in GraphQL language implemented in this API.


1. Generate JWT token. Currently works for all usernames and passwords. When the token expires, refresh token is enough to generate new access token. (See 6)

    ```graphql
     mutation {
          login(password: "", username: "") {
             accessToken
             refreshToken
          }
       }
    ```

**Important step**

2. After the generation of JWT token, a authentication header needs to be set from the client side application. Every request to this server must have this auth header. 

For example, from Apollo Angular client.

```js
const auth = setContext((operation, context) => {
    const token = localStorage.getItem('accessToken');

    if (token === null) {
      return {};
    } else {
      return {
        headers: new HttpHeaders().set('Authorization', `Bearer ${token}`)
      };
    }
  });
```

3. The following queries have been implemented to support qualiexplore.

```graphql
     query {
        users {
          users {
            username
            password
          }
        }
      }
```

For more information see GraphQL client documentation page.
