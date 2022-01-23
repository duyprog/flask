from flask import Flask
from security import authenticate, identity
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
# pip install Flask_RESTFul
# pip install Flask_JWT

app = Flask(__name__)
app.secret_key = 'duypk'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create a new endpoint /auth
# jwt get our username and password, and send it to authenticate function, find correct user object and compare password that we received
# /auth endpoint will return JWT token if password is matched
# We can send jwt token to the next request we make, when we send jwt token, jwt will call identity function
# It will use JWT token to get the user id that means the user was authenticated, JWT token is valid 

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
app.run(port=5000,debug=True) # Debug de show error message 
